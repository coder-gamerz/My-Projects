import customtkinter as ctk
import pandas as pd
import numpy as np
import re
import string
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
import time

# Function to clean text
def wordopt(text):
    text = text.lower()
    text = re.sub('\[.*?\]', '', text)
    text = re.sub("\\W", " ", text)
    text = re.sub('https?://\S+|www\.\S+', '', text)
    text = re.sub('<.*?>+', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\w*\d\w*', '', text)
    return text

# Load and preprocess datasets
def load_and_preprocess_data():
    data_fake = pd.read_csv(r'datasets/Fake.csv')
    data_true = pd.read_csv(r'datasets/True.csv')

    data_fake["class"] = 0
    data_true["class"] = 1

    data_fake = data_fake.iloc[:-10]  # Removing last 10 entries for manual testing
    data_true = data_true.iloc[:-10]  # Removing last 10 entries for manual testing

    data_merge = pd.concat([data_fake, data_true], axis=0).sample(frac=1).reset_index(drop=True)
    data = data_merge.drop(['title', 'subject', 'date'], axis=1)
    data['text'] = data['text'].apply(wordopt)

    return data

# Load data
data = load_and_preprocess_data()

# Splitting the data
x = data['text']
y = data['class']
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25)

# Vectorization
vectorization = TfidfVectorizer()
xv_train = vectorization.fit_transform(x_train)
xv_test = vectorization.transform(x_test)

# Model training and prediction
def train_and_evaluate_model(model, xv_train, y_train, xv_test, y_test):
    start_time = time.time()
    model.fit(xv_train, y_train)
    pred = model.predict(xv_test)
    elapsed_time = time.time() - start_time
    print(f"{model.__class__.__name__}:\n", classification_report(y_test, pred))
    print(f"Time taken: {elapsed_time:.2f} seconds\n")
    return model

# Instantiate models
LR = LogisticRegression()
DT = DecisionTreeClassifier()
GB = GradientBoostingClassifier(random_state=0)
RF = RandomForestClassifier(random_state=0)

# Train and evaluate models
models = [LR, DT, GB, RF]
for model in models:
    train_and_evaluate_model(model, xv_train, y_train, xv_test, y_test)

# Output label function
def output_label(n):
    return "Fake News" if n == 0 else "Not Fake News"

# Manual testing function
def manual_testing(news, vectorization, models):
    testing_news = {"text": [news]}
    new_def_test = pd.DataFrame(testing_news)
    new_def_test['text'] = new_def_test['text'].apply(wordopt)
    new_xv_test = vectorization.transform(new_def_test['text'])
    predictions = [model.predict(new_xv_test)[0] for model in models]
    model_names = [model.__class__.__name__ for model in models]
    result_text = ""
    
    if 1 in predictions:
        result_text += "Overall Prediction: Real News"
    else:
        result_text += "Overall Prediction: Fake News"
    
    return result_text

# Create the GUI application
def clear_text():
    textbox.delete("1.0", ctk.END)

def evaluate_text():
    news = textbox.get("1.0", ctk.END).strip()
    if news:
        result = manual_testing(news, vectorization, models)
        result_label.configure(text=result)

app = ctk.CTk()
app.geometry("600x500")
app.title("Fake News Detection")

textbox = ctk.CTkTextbox(app, width=500, height=200)
textbox.pack(pady=20)

clear_button = ctk.CTkButton(app, text="Clear", command=clear_text)
clear_button.pack(pady=5)

evaluate_button = ctk.CTkButton(app, text="Evaluate", command=evaluate_text)
evaluate_button.pack(pady=5)

result_label = ctk.CTkLabel(app, text="", wraplength=500)
result_label.pack(pady=20)

app.mainloop()
