from pgmpy.models import BayesianModel
from pgmpy.estimators import MaximumLikelihoodEstimator
from pgmpy.estimators import BayesianEstimator
from pgmpy.inference import VariableElimination
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import pandas as pd
import numpy as np
import json

# Load labeled text data (positive, negative, neutral)
def load_data(filename):
    df = pd.read_csv(filename)
    X = df['text'].values
    y = df['sentiment'].values
    return X, y

# Preprocess text data and extract features
def preprocess_text(X):
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(X)
    return X, vectorizer

# Train Bayesian network model with enhanced features
def train_model(X, y):
    model = BayesianModel([('features', 'sentiment')])
    model.fit(X, y, estimator=BayesianEstimator, prior_type="BDeu")
    return model

# Perform sentiment analysis
def sentiment_analysis(text, model, vectorizer):
    inference = VariableElimination(model)
    evidence = {'features': vectorizer.transform([text])}
    result = inference.map_query(variables=['sentiment'], evidence=evidence)
    return result['sentiment']

# Evaluate model using cross-validation
def evaluate_model(X, y, model, vectorizer):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model.fit(X_train, y_train, estimator=BayesianEstimator, prior_type="BDeu")
    y_pred = []
    for text in X_test:
        sentiment = sentiment_analysis(text, model, vectorizer)
        y_pred.append(sentiment)
    print(classification_report(y_test, y_pred))

# Error analysis
def error_analysis(X, y, model, vectorizer):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model.fit(X_train, y_train, estimator=BayesianEstimator, prior_type="BDeu")
    incorrect_samples = []
    for i, text in enumerate(X_test):
        sentiment = sentiment_analysis(text, model, vectorizer)
        if sentiment != y_test[i]:
            incorrect_samples.append((text, y_test[i], sentiment))
    return incorrect_samples

# Interpretability
def explain_prediction(text, model, vectorizer):
    features = vectorizer.transform([text])
    evidence = {'features': features}
    inference = VariableElimination(model)
    query = inference.map_query(variables=['sentiment'], evidence=evidence)
    sentiment = query['sentiment']
    return sentiment

if __name__ == '__main__':
    X, y = load_data('labeled_data.csv')
    X, vectorizer = preprocess_text(X)
    model = train_model(X, y)

    # Error analysis
    incorrect_samples = error_analysis(X, y, model, vectorizer)
    print("Incorrect samples:")
    for sample in incorrect_samples:
        print(f"Text: {sample[0]}, True Sentiment: {sample[1]}, Predicted Sentiment: {sample[2]}")

    # Interpretability
    text = "This product is great!"
    explanation = explain_prediction(text, model, vectorizer)
    print(f"Explanation for '{text}': Predicted Sentiment: {explanation}")
