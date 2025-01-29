# Import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import string
import nltk
from nltk.corpus import stopwords
from nltk import PorterStemmer as Stemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib  # For saving and loading models

# Download required NLTK data
nltk.download('stopwords')

# Load and preprocess the dataset
def load_dataset(path):
    """Load the dataset and return a preprocessed DataFrame."""
    df = pd.read_csv(path, encoding='latin-1')[['v1', 'v2']]
    df.columns = ['label', 'message']
    return df

# Text preprocessing function
def process(text):
    """Preprocess text by removing punctuation, stopwords, and applying stemming."""
    text = text.lower()  # Lowercase text
    text = ''.join([t for t in text if t not in string.punctuation])  # Remove punctuation
    text = [t for t in text.split() if t not in stopwords.words('english')]  # Remove stopwords
    st = Stemmer()
    text = [st.stem(t) for t in text]  # Apply stemming
    return text

# Visualize label distribution
def visualize_label_distribution(df):
    """Plot the distribution of labels in the dataset."""
    label_counts = df['label'].value_counts()
    plt.figure(figsize=(8, 6))
    sns.barplot(x=label_counts.index, y=label_counts.values, hue=label_counts.index, palette="viridis", dodge=False)
    plt.title("Label Distribution: Ham vs Spam")
    plt.xlabel("Label")
    plt.ylabel("Number of Emails")
    plt.show()

# Train the spam filter model
def train_model(df):
    """Train a spam filter model and return the trained pipeline."""
    # Split dataset into training and test sets
    x_train, x_test, y_train, y_test = train_test_split(df['message'], df['label'], test_size=0.20, random_state=21)
    
    # Build the pipeline
    spam_filter = Pipeline([
        ('vectorizer', TfidfVectorizer(analyzer=process)),  # Convert text to TF-IDF
        ('classifier', MultinomialNB())  # Train Naive Bayes classifier
    ])
    
    # Train the model
    spam_filter.fit(x_train, y_train)
    print("Model training complete.")
    
    # Evaluate the model
    predictions = spam_filter.predict(x_test)
    print("Classification Report:")
    print(classification_report(y_test, predictions))
    
    # Return the trained model and test data for further evaluation
    return spam_filter, x_test, y_test, predictions

# Save the trained model to a file
def save_model(model, filename):
    """Save the trained model to a file."""
    joblib.dump(model, filename)
    print(f"Model saved to {filename}.")

# Load a saved model
def load_model(filename):
    """Load a model from a file."""
    model = joblib.load(filename)
    print(f"Model loaded from {filename}.")
    return model

# Main execution
if __name__ == "__main__":
    # Define dataset path
    dataset_path = r'C:\Users\ameni\zormati\spam.csv'
    
    # Load the dataset
    df = load_dataset(dataset_path)
    print("First few rows of the dataset:")
    print(df.head())
    
    # Visualize label distribution
    visualize_label_distribution(df)
    
    # Train the model
    spam_filter, x_test, y_test, predictions = train_model(df)
    
    # Save the trained model
    model_filename = 'spam_filter_model.pkl'
    save_model(spam_filter, model_filename)
    
    # Example usage of the saved model
    test_message = "Your cash-balance is currently 500 pounds - to maximize your cash-in now, send COLLECT to 83600."
    spam_filter_loaded = load_model(model_filename)
    prediction = spam_filter_loaded.predict([test_message])
    print(f"Prediction for test message: {test_message}")
    print(f"Classified as: {prediction[0]}")
