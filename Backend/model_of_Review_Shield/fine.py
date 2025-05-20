import torch
from transformers import DistilBertTokenizerFast, DistilBertForSequenceClassification
from torch.utils.data import DataLoader, Dataset, random_split
from transformers import AdamW
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, f1_score
import pandas as pd
from tqdm import tqdm

# Custom Dataset
class ReviewDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_len=512):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_len = max_len

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        text = self.texts[idx]
        label = self.labels[idx]
        encoding = self.tokenizer(
            text,
            padding='max_length',
            truncation=True,
            max_length=self.max_len,
            return_tensors='pt'
        )
        return {
            'input_ids': encoding['input_ids'].squeeze(0),
            'attention_mask': encoding['attention_mask'].squeeze(0),
            'label': torch.tensor(label, dtype=torch.long)
        }

# Load dataset
file_path = "fake_reviews_dataset.csv"
data = pd.read_csv(file_path)
data['label'] = data['label'].map({'OR': 0, 'CG': 1})
texts = data['text_'].tolist()
labels = data['label'].tolist()

# Split dataset
train_texts, val_texts, train_labels, val_labels = train_test_split(texts, labels, test_size=0.2, stratify=labels)

# Load tokenizer and model
tokenizer = DistilBertTokenizerFast.from_pretrained("distilbert-base-uncased")
model = DistilBertForSequenceClassification.from_pretrained("distilbert-base-uncased", num_labels=2)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Device in use:", device)
model.to(device)

# Prepare datasets
train_dataset = ReviewDataset(train_texts, train_labels, tokenizer, max_len=256)
val_dataset = ReviewDataset(val_texts, val_labels, tokenizer, max_len=256)
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True, pin_memory=True)
val_loader = DataLoader(val_dataset, batch_size=32, pin_memory=True)

# Use class weights
class_counts = pd.Series(train_labels).value_counts().sort_index()
weights = 1. / class_counts
weights = torch.tensor(weights.values, dtype=torch.float).to(device)
criterion = torch.nn.CrossEntropyLoss(weight=weights)

optimizer = AdamW(model.parameters(), lr=2e-5)

# Training loop with early stopping
best_f1 = 0
patience = 2
wait = 0

for epoch in range(4):  # max 10 epochs
    model.train()
    total_loss = 0
    for batch in tqdm(train_loader, desc=f"Training Epoch {epoch+1}"):
        input_ids = batch['input_ids'].to(device)
        attention_mask = batch['attention_mask'].to(device)
        labels = batch['label'].to(device)

        optimizer.zero_grad()
        outputs = model(input_ids=input_ids, attention_mask=attention_mask)
        loss = criterion(outputs.logits, labels)
        loss.backward()
        optimizer.step()

        total_loss += loss.item()

    avg_loss = total_loss / len(train_loader)
    print(f"\nEpoch {epoch+1} Training Loss: {avg_loss:.4f}")

    # Evaluation
    model.eval()
    preds, true = [], []
    with torch.no_grad():
        for batch in val_loader:
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            labels = batch['label'].to(device)

            outputs = model(input_ids=input_ids, attention_mask=attention_mask)
            predictions = torch.argmax(outputs.logits, dim=-1)

            preds.extend(predictions.cpu().numpy())
            true.extend(labels.cpu().numpy())

    f1 = f1_score(true, preds, average='weighted')
    print("\nValidation Results:")
    print(classification_report(true, preds))
    print(f"Weighted F1 Score: {f1:.4f}")

    # Early stopping logic
    if f1 > best_f1:
        best_f1 = f1
        wait = 0
        print("New best model found. Saving...")
        model.save_pretrained("fine_tuned_model")
        tokenizer.save_pretrained("fine_tuned_model")
    else:
        wait += 1
        print(f"No improvement. Patience {wait}/{patience}")
        if wait >= patience:
            print("Early stopping triggered.")
            break
