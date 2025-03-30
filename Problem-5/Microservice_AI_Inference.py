from fastapi import FastAPI, HTTPException
import joblib, requests

app = FastAPI()
model = joblib.load('ai_model.joblib')

def transform_data_into_features(data):
    # extract features and return
    pass

# Feature Extraction
@app.post("/preprocess_data")
async def preprocess_data():
    # Retrieve Payload JSON
    payload = requests.get_json()
    
    features = transform_data_into_features(payload)
    return {"processed_features": features}

# Inference
@app.post("/predict")
async def predict(data: dict):
    try:
        prediction = model.predict(data["processed_features"])
        return {"prediction": prediction}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))