import requests
import json

def inference(data):
    # Preprocess data
    features = requests.post("{URL}/preprocess_data", json={"data": data})

    if features.status_code != 200:
        raise Exception(f"Preprocessing failed: {features.text}")
    
    processed_data = features.json()["processed_features"]

    # AI Inference
    prediction = requests.post("{URL}/predict", json={"processed_features": processed_data})
    if prediction.status_code != 200:
        raise Exception(f"Prediction failed: {prediction.text}")
    
    predicted_value = prediction.json()["prediction"]
    return predicted_value

if __name__ == "__main__":
    data = [] # Dummy data
    prediction = inference(data)
    print(f"Predicted Value : {prediction}")