from flask import Flask, request, jsonify
import pickle

app = Flask(__name__)

model = pickle.load(open('vinod.pkl', 'rb'))

# 1. Accept a POST request with input data in JSON format
@app.route('/predict', methods = ['POST'])
def predict():
    try
        # Retrieve Payload JSON
        payload = request.get_json()
        data_for_model = parse_input(payload)

        # 2. Use the model to generate a prediction 
        predicted_result = model.predict(data_for_model)

        # 3. Return the prediction in JSON format
        return jsonify({'prediction': predicted_result})
    catch():
        return Exception

# For Parsing input json and return in model input format
def parse_input(payload):
    #Check Error and send error
    pass

if __name__ == '__main__':
    app.run(debug=True)