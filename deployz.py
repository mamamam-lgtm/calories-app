from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import joblib
import numpy as np
import pandas as pd

# Define the expected request structure
class InputData(BaseModel):
    Gender: int
    Age: int
    Height: float
    Weight: float
    Duration: float
    Heart_Rate: float
    Body_Temp: float

app = FastAPI()

# Load model and scaler
model = joblib.load("xgb_model.pkl")
scaler = joblib.load("scaler.pkl")

@app.get("/")
def home():
    return {"message": "Calorie Prediction API is running!"}

@app.post("/predict/")
def predict(data: List[InputData]):
    # Convert list of InputData into DataFrame
    df = pd.DataFrame([d.dict() for d in data])

    # Scale the input
    scaled = scaler.transform(df)

    # Predict
    predictions = model.predict(scaled)

    return {"Predicted Calories": predictions.tolist()}
