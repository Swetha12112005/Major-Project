# 🎓 PlaceMate AI — Student Placement Prediction Suite

> **Live Demo:**  https://placemate-ai.onrender.com/
> 

An AI-powered career suite for engineering students — predict placement chances, optimize your resume for ATS, and track your career journey.

---

## 🚀 Features

- **🧠 Placement Predictor** — Enter your CGPA, skills, internships, and projects to get an ML-powered placement probability score
- **📄 ATS Resume Optimizer** — Upload your resume and get a keyword match score with role-specific suggestions
- **🗺️ Career Roadmap** — Personalized learning paths based on your target role (Frontend, Backend, Data Science, DevOps, etc.)
- **📅 Progress Timeline** — Log and track your daily learning updates

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | HTML5, CSS3, Vanilla JavaScript |
| Backend | Python, FastAPI, Uvicorn |
| ML Model | XGBoost (trained on student placement data) |
| Resume Parsing | PyPDF, docx2txt |
| Tunneling | ngrok |

---

## ⚙️ How to Run Locally

### 1. Install dependencies
```bash
pip install fastapi uvicorn xgboost pandas joblib pypdf docx2txt python-dotenv
```

### 2. Start the server
```bash
python main.py
```

### 3. Open in browser
```
http://localhost:10000
```

### 4. (Optional) Make it public with ngrok
```bash
ngrok http 10000
```

---

## 📁 Project Structure

```
student_placement_full_project/
├── main.py                     # FastAPI backend server
├── index.html                  # Frontend UI
├── styles.css                  # Stylesheet
├── script.js                   # JavaScript logic
├── app.py                      # Flask student data API
├── data.json                   # Student dataset
├── xgboost_placement_model.pkl # Trained ML model
├── preprocessor.pkl             # Data preprocessor
 ---render.yaml        
└── README.md
```

---
## Deploy on Render
   This repository already includes render.yaml, so Render can deploy it as a web service and provide a stable public URL.
  1. Push the latest code to GitHub:
     '''
     git add .
     git commit -m "Prepare app for Render deployment"
     git push origin master
     '''
  2. In Render:
     Create a new Web Service
     Select the GitHub repository placemate-ai
     Confirm the detected settings from render.yaml
     Deploy
3.After deployment, Render will give you a permanent URL similar to:
     https://placemate-ai.onrender.com
4.Optional:
   Add a custom domain in the Render service settings

## 👩‍💻 Developer

**Swetha** — Engineering Student | AI/ML Enthusiast

---

© 2024 PlaceMate AI. Built for students, by a student.
