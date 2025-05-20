# 1. Imports
import torch
from datasets import load_dataset, DatasetDict
from transformers import (
    DistilBertTokenizerFast,
    DistilBertForSequenceClassification,
    TrainingArguments,
    Trainer
)
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

# 2. Load and preprocess the dataset
dataset = load_dataset("csv", data_files={"train": "fake_vs_real_reviews_20k_clean.csv"}, split="train")

def encode_labels(example):
    example["label"] = 0 if example["label"] == "real" else 1
    return example

dataset = dataset.map(encode_labels)

# 3. Tokenize
tokenizer = DistilBertTokenizerFast.from_pretrained("distilbert-base-uncased")

def tokenize(example):
    return tokenizer(example["text"], padding="max_length", truncation=True)

dataset = dataset.map(tokenize, batched=True)
dataset.set_format(type="torch", columns=["input_ids", "attention_mask", "label"])

# 4. Train-test split
train_test = dataset.train_test_split(test_size=0.2)
train_dataset = train_test["train"]
eval_dataset = train_test["test"]

# 5. Load model and training args
model = DistilBertForSequenceClassification.from_pretrained("distilbert-base-uncased", num_labels=2)

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    preds = torch.argmax(torch.tensor(logits), axis=1)
    precision, recall, f1, _ = precision_recall_fscore_support(labels, preds, average="binary")
    acc = accuracy_score(labels, preds)
    return {"accuracy": acc, "f1": f1, "precision": precision, "recall": recall}

training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=3,
    weight_decay=0.01,
    fp16=True,  # Use mixed precision if your GPU supports it
)

# 6. Trainer setup and training
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    compute_metrics=compute_metrics,
)

trainer.train()

# Save model and tokenizer after training
model.save_pretrained("saved_model")
tokenizer.save_pretrained("saved_model")

# 7. Inference function
def predict_review(text):
    tokens = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    tokens = {k: v.to(model.device) for k, v in tokens.items()}
    output = model(**tokens)
    pred = torch.argmax(output.logits, dim=1).item()
    return "Real (Human)" if pred == 0 else "Fake (AI)"

# Example usage
print(predict_review("This is the best vacuum cleaner I’ve ever used!"))
