
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import joblib
import xgboost as xgb
import uvicorn
import re

app = FastAPI(title="Student Placement Prediction API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load XGBoost Model
try:
    model = joblib.load("xgboost_placement_model.pkl")
except:
    model = None

@app.post("/predict")
async def predict(data: dict):
    if model is None:
        return {"error": "Model file not found. Add xgboost_placement_model.pkl"}

    df = pd.DataFrame([data])
    prediction = model.predict(df)[0]
    probability = model.predict_proba(df)[0][1]

    return {
        "placement_status": int(prediction),
        "placement_probability": float(round(probability, 3))
    }

@app.post("/resume-analyzer")
async def analyze_resume(file: UploadFile = File(...)):
    content = await file.read()
    text = content.decode("utf-8", errors="ignore")

    keywords = ["python", "machine learning", "data science",
                "internship", "project", "sql", "communication"]

    score = sum(1 for word in keywords if word.lower() in text.lower())
    resume_score = round((score / len(keywords)) * 100, 2)

    return {
        "resume_score_percentage": resume_score,
        "suggestion": "Add more technical keywords and quantified achievements."
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
