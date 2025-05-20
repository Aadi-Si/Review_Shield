import torch
from transformers import DistilBertForSequenceClassification, DistilBertTokenizerFast
import torch.nn.functional as F
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import pandas as pd

# Load saved model and tokenizer
model = DistilBertForSequenceClassification.from_pretrained("fine_tuned_model")
tokenizer = DistilBertTokenizerFast.from_pretrained("fine_tuned_model")

# Move model to GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
model.eval()

# Inference function with confidence score (percentage)
def predict_review_with_score(text):
    tokens = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    tokens = {k: v.to(device) for k, v in tokens.items()}

    output = model(**tokens)
    logits = output.logits
    probs = F.softmax(logits, dim=-1)

    real_prob = probs[0][0].item()
    fake_prob = probs[0][1].item()

    real_score = real_prob * 100
    fake_score = fake_prob * 100

    return real_score, fake_score, int(fake_prob > real_prob)  # 1 for fake, 0 for real

# Load dataset
file_path = "fake_reviews_dataset.csv"  # Update with your correct path if needed
data = pd.read_csv(file_path)

# Map string labels to numeric: CG (fake) -> 1, OR (real) -> 0
label_map = {'CG': 1, 'OR': 0}
data['label'] = data['label'].map(label_map)

texts = data['text_'].tolist()
true_labels = data['label'].tolist()

# Predict on all data
pred_labels = []
for text in texts:
    _, _, pred = predict_review_with_score(text)
    pred_labels.append(pred)

# Calculate metrics
accuracy = accuracy_score(true_labels, pred_labels)*100
report = classification_report(true_labels, pred_labels)
conf_matrix = confusion_matrix(true_labels, pred_labels)

print(f"Accuracy: {accuracy:.2f}")
print("\nClassification Report:\n", report)
print("\nConfusion Matrix:\n", conf_matrix)