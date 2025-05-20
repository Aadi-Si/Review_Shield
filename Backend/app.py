from flask import Flask, request, render_template, jsonify
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import torch
from transformers import DistilBertForSequenceClassification, DistilBertTokenizerFast
import torch.nn.functional as F
import os
from flask_cors import CORS
import time

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Load model and tokenizer at startup
MODEL_PATH = os.path.join("model_of_Review_Shield", "fine_tuned_model")
model = DistilBertForSequenceClassification.from_pretrained(MODEL_PATH)
tokenizer = DistilBertTokenizerFast.from_pretrained(MODEL_PATH)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
model.eval()

def predict_review_with_score(text):
    tokens = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    tokens = {k: v.to(device) for k, v in tokens.items()}

    with torch.no_grad():
        output = model(**tokens)
        probs = F.softmax(output.logits, dim=-1)
        real_score = probs[0][0].item() * 100
        fake_score = probs[0][1].item() * 100

    return real_score, fake_score

@app.route("/", methods=['GET'])
def home():
    return render_template('index.html')

@app.route("/review", methods=['POST'])
def review():
    try:
        product_link = request.form['content']
        return analyze_product(product_link, render_html=True)
    except Exception as e:
        print("Error in /review:", e)
        return render_template('results.html', product_name=None, reviews=[], error=str(e))

@app.route("/api/review", methods=['POST'])
def api_review():
    try:
        data = request.get_json()
        product_link = data['url']
        return analyze_product(product_link, render_html=False)
    except Exception as e:
        print("Error in /api/review:", e)
        return jsonify({"error": str(e)}), 500

def analyze_product(product_link, render_html=False, max_pages=10, max_reviews=200):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    reviews = []
    comments_only = []
    image_urls = []
    product_name = "Unknown Product"

    try:
        driver.get(product_link)
        soup = bs(driver.page_source, 'html.parser')

        try:
            all_reviews_button = driver.find_element("css selector", "div.RcXBOT")
            all_reviews_button.click()
            time.sleep(2)
            soup = bs(driver.page_source, 'html.parser')
        except Exception as e:
            print("No 'All reviews' button found:", e)

        review_links = soup.select('nav.WSL9JP a')
        base_review_url = None
        for link in review_links:
            if "page=" in link.get("href", ""):
                base_review_url = "https://www.flipkart.com" + link["href"].split("?page=")[0] + "?page="
                break

        if not base_review_url:
            base_review_url = product_link.split("?")[0] + "?page="

        for page in range(1, max_pages + 1):
            driver.get(base_review_url + str(page))
            time.sleep(2)
            soup = bs(driver.page_source, 'html.parser')

            if page == 1:
                product_name_tag = soup.find("div", {"class": "C7fEHH"})
                product_name = product_name_tag.div.text.strip() if product_name_tag and product_name_tag.div else product_name

                try:
                    image_tags = soup.find_all("img", {"class": "DByuf4 IZexXJ jLEJ7H"})
                    image_urls = [img['src'] for img in image_tags if img.get('src')]
                except:
                    image_urls = []

            comment_boxes = soup.findAll("div", {"class": "RcXBOT"})
            if not comment_boxes:
                break

            for comment_box in comment_boxes:
                try:
                    name = comment_box.div.div.find_all('p', {'class': '_2NsDsF AwS1CA'})[0].text
                except:
                    name = 'No Name'

                try:
                    rating = comment_box.div.div.div.div.text
                except:
                    rating = 'No Rating'

                try:
                    comment_head = comment_box.div.div.div.p.text
                except:
                    comment_head = 'No Comment Heading'

                try:
                    zmyheo_div = comment_box.find('div', class_='ZmyHeo')
                    read_more_span = zmyheo_div.find('span', class_='wTYmpv')
                    if read_more_span:
                        read_more_span.extract()
                    comment = zmyheo_div.text.strip()
                except:
                    comment = ''

                if not comment:
                    continue

                comments_only.append(comment)
                reviews.append({
                    "Name": name,
                    "Rating": rating,
                    "CommentHead": comment_head,
                    "Comment": comment
                })

                if len(reviews) >= max_reviews:
                    break
            if len(reviews) >= max_reviews:
                break

    finally:
        driver.quit()

    real_count = 0
    for comment in comments_only:
        real_score, _ = predict_review_with_score(comment)
        if real_score > 50:
            real_count += 1

    total_comments = len(comments_only)
    fake_count = total_comments - real_count
    real_percent = (real_count / total_comments) * 100 if total_comments else 0
    fake_percent = 100 - real_percent

    grade = (
        "A+" if real_percent > 90 else
        "A" if real_percent > 80 else
        "B" if real_percent > 70 else
        "C" if real_percent > 60 else
        "D"
    )
    overall_rating = "✅ Recommended to Buy" if real_count >= total_comments / 2 else "❌ Not Recommended"

    if render_html:
        return render_template(
            'results.html',
            product_name=product_name,
            reviews=reviews,
            images=image_urls,
            overall_rating=overall_rating
        )
    else:
        return jsonify({
            "product_name": product_name,
            "reviews": reviews,
            "images": image_urls,
            "overall_rating": overall_rating,
            "stats": {
                "total": total_comments,
                "real": real_count,
                "fake": fake_count,
                "real_percent": real_percent,
                "fake_percent": fake_percent,
                "grade": grade
            }
        })

if __name__ == "__main__":
    app.run(debug=True)
