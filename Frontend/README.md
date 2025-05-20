# 🛡️ Review Shield – Fake Review Detection System

Review Shield is an AI-powered web application that detects fake (AI-generated or manipulated) product reviews on Flipkart using natural language processing. It scrapes real-time reviews and classifies them using a fine-tuned DistilBERT model.

![Review Shield Banner](/assets/Landing_page.png)

---

## 📸 Demo Screenshots

### 🧠 Model Training Accuracy

![Training model-1](/assets/training-1.png)
![Training model-2](/assets/training-2.png)

### 📉 Model Loss

![Model Accuracy](/assets/accuracy.png)

### 🌐 Credibility Score Of Product 

![output](/assets/product%20review%20output.png)

---

## 🚀 Features

- 🔗 Paste Flipkart product URL and analyze reviews.
- 🤖 Classify reviews as **Real** (Human-written) or **Fake** (AI-generated or suspicious).
- 📊 Visual summary via pie charts.
- 📥 Real-time scraping using Selenium and BeautifulSoup.
- 🧠 Uses a fine-tuned DistilBERT transformer model.

---

## 🧰 Tech Stack

### 🔵 Frontend
- React.js
- Axios
- Recharts (for data visualization)

### 🔴 Backend
- Flask (Python)
- Selenium (for dynamic review loading)
- BeautifulSoup (for parsing HTML)
- HuggingFace Transformers (DistilBERT)
- scikit-learn, pandas, numpy (for preprocessing and analysis)

### 🤖 Model
- DistilBERT Base (fine-tuned on fake vs real reviews dataset)
- Binary Classification (Real / Fake)
- Trained using HuggingFace + PyTorch

---



