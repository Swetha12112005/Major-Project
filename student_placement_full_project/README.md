# 🎓 PlaceMate AI — Student Placement Prediction Suite

> **Live Demo:**  https://placemate-ai.onrender.com/
> *(Note: This is a temporary ngrok URL. Contact the developer if it's offline.)*

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
├── preprocessor.pkl            # Data preprocessor
└── README.md
```

---

## 👩‍💻 Developer

**Swetha** — Engineering Student | AI/ML Enthusiast

---

© 2024 PlaceMate AI. Built for students, by a student.
