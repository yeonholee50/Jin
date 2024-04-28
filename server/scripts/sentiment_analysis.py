from pgmpy.models import BayesianModel
from pgmpy.estimators import MaximumLikelihoodEstimator
import json

# Define Bayesian network structure
model = BayesianModel([('text', 'sentiment')])

# Load pre-trained model from JSON file
def load_model(filename):
    with open(filename, 'r') as file:
        model_data = json.load(file)
    model = BayesianModel()
    model.add_nodes_from(model_data['nodes'])
    model.add_edges_from(model_data['edges'])
    model.fit_cpds(model_data['cpds'])
    return model

model = load_model('sentiment_model.json')

# Perform sentiment analysis
def sentiment_analysis(text):
    inference = VariableElimination(model)
    evidence = {'text': text}
    result = inference.map_query(variables=['sentiment'], evidence=evidence)
    return result['sentiment']

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print('Usage: python sentiment_analysis.py <text>')
        sys.exit(1)
    text = sys.argv[1]
    sentiment = sentiment_analysis(text)
    print(sentiment)
