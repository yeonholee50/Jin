# sentiment_analysis.py
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
    return X

# Train Bayesian network model with enhanced features
def train_model(X, y):
    model = BayesianModel([('features', 'sentiment')])
    model.fit(X, y, estimator=BayesianEstimator, prior_type="BDeu")
    return model


# Perform sentiment analysis
def sentiment_analysis(text, model):
    inference = VariableElimination(model)
    evidence = {'features': text}
    result = inference.map_query(variables=['sentiment'], evidence=evidence)
    return result['sentiment']

# Evaluate model using cross-validation
def evaluate_model(X, y, model):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model.fit(X_train, y_train, estimator=BayesianEstimator, prior_type="BDeu")
    y_pred = []
    for text in X_test:
        sentiment = sentiment_analysis(text, model)
        y_pred.append(sentiment)
    print(classification_report(y_test, y_pred))

if __name__ == '__main__':
    X, y = load_data('labeled_data.csv')
    X = preprocess_text(X)
    model = train_model(X, y)
    evaluate_model(X, y, model)
