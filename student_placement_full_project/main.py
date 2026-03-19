
from fastapi import FastAPI, UploadFile, File, Form, Depends, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import pandas as pd
import joblib
import xgboost as xgb
import uvicorn
import re
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Student Placement Prediction API")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Serve the frontend folder as static files
app.mount("/static", StaticFiles(directory=BASE_DIR), name="static")

@app.get("/")
def serve_frontend():
    return FileResponse(os.path.join(BASE_DIR, "index.html"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = os.getenv("API_KEY", "default_dev_key")
api_key_scheme = APIKeyHeader(name="x-api-key", auto_error=False)

async def get_api_key(api_key: str = Security(api_key_scheme)):
    if api_key == API_KEY:
        return api_key
    raise HTTPException(status_code=403, detail="Could not validate API Key")

# Load ML Assets
try:
    model = joblib.load("xgboost_placement_model.pkl")
    preprocessor = joblib.load("preprocessor.pkl")
except Exception as e:
    print(f"Error loading model/preprocessor: {e}")
    model = None
    preprocessor = None

@app.post("/predict")
async def predict(data: dict, api_key: str = Depends(get_api_key)):
    if model is None or preprocessor is None:
        return {"error": "Model or Preprocessor files not found."}

    # Extract raw features from request
    raw_df = pd.DataFrame([data])
    
    # --- MAPPING & CLEANING ---
    # Map frontend departments to model categories: CSE, IT, ECE, EEE, MECH
    dept_map = {
        'cse_gen': 'CSE', 'cse_ai': 'CSE', 'cse_ml': 'CSE', 'cse_ds': 'CSE', 'cse_cyber': 'CSE',
        'it': 'IT', 'ise': 'IT',
        'ece': 'ECE', 'eie': 'ECE',
        'eee': 'EEE',
        'mech': 'MECH', 'civil': 'MECH', 'chem': 'MECH', 'other': 'MECH'
    }
    raw_df['department'] = raw_df['department'].map(dept_map).fillna('MECH')
    
    # Map frontend skills to model categories: Web Dev, Data Science, Cloud, Core, Cyber
    skill_map = {
        'mern': 'Web Dev', 'mean': 'Web Dev', 'react': 'Web Dev', 'angular': 'Web Dev', 
        'vue': 'Web Dev', 'php_laravel': 'Web Dev', 'node_express': 'Web Dev', 'python_django': 'Web Dev', 'rest_apis': 'Web Dev',
        'data_science': 'Data Science', 'ml_engineer': 'Data Science', 'data_analysis': 'Data Science', 'bigdata': 'Data Science',
        'aws': 'Cloud', 'azure': 'Cloud', 'devops': 'Cloud', 'sre': 'Cloud',
        'cyber_sec': 'Cyber',
        'qa_testing': 'Core', 'blockchain': 'Core', 'flutter': 'Core', 'android': 'Core', 'ios': 'Core', 'cad_design': 'Core', 'embedded': 'Core', 'vlsi': 'Core'
    }
    raw_df['skill_stack'] = raw_df['skill_stack'].map(skill_map).fillna('Core')

    # Ensure numeric types
    for col in ['cgpa', 'internships', 'projects', 'aptitude_score', 'communication_score', 'active_backlogs']:
        raw_df[col] = pd.to_numeric(raw_df[col], errors='coerce').fillna(0)

    # --- FEATURE ENGINEERING (Must match Training Logic) ---
    raw_df['composite_score'] = (
        raw_df['cgpa'] * 10 +
        raw_df['internships'] * 15 +
        raw_df['projects'] * 2 +
        raw_df['aptitude_score'] * 0.3 +
        raw_df['communication_score'] * 2 -
        raw_df['active_backlogs'] * 18
    )
    raw_df['cgpa_x_internship'] = raw_df['cgpa'] * raw_df['internships']
    raw_df['aptitude_x_projects'] = raw_df['aptitude_score'] * raw_df['projects']

    # --- PREPROCESS & PREDICT ---
    try:
        # Transform data using training preprocessor
        X_processed = preprocessor.transform(raw_df)
        
        prediction = model.predict(X_processed)[0]
        probability = model.predict_proba(X_processed)[0][1]

        return {
            "placement_status": int(prediction),
            "placement_probability": float(round(probability, 3))
        }
    except Exception as e:
        return {"error": f"Prediction failed: {str(e)}"}

@app.post("/resume-analyzer")
async def analyze_resume(file: UploadFile = File(...), role: str = Form("default")):
    content = await file.read()
    
    text = ""
    filename = file.filename.lower() if file.filename else ""
    
    if filename.endswith(".pdf"):
        from io import BytesIO
        from pypdf import PdfReader
        try:
            reader = PdfReader(BytesIO(content))
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + " "
        except Exception as e:
            text = ""
    elif filename.endswith(".docx"):
        from io import BytesIO
        import docx2txt
        try:
            text = docx2txt.process(BytesIO(content))
        except Exception as e:
            text = ""
    else:
        text = content.decode("utf-8", errors="ignore")

    # Role-specific keyword datasets
    role_keywords = {
        "frontend": ["html", "css", "javascript", "react", "vue", "angular", "responsive", "ui", "ux", "web performance", "dom", "frontend", "redux", "tailwind", "bootstrap", "typescript"],
        "backend": ["python", "java", "node", "express", "sql", "mongodb", "postgresql", "mysql", "api", "rest", "graphql", "server", "django", "spring boot", "ruby", "c#", ".net"],
        "fullstack": ["react", "node", "express", "mongodb", "sql", "api", "javascript", "python", "html", "css", "git", "aws", "docker", "frontend", "backend", "full stack", "mern"],
        "data-scientist": ["python", "r", "sql", "machine learning", "statistics", "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch", "data visualization", "tableau", "deep learning", "nlp"],
        "ml-engineer": ["python", "c++", "machine learning", "deep learning", "tensorflow", "pytorch", "model deployment", "mlops", "aws", "docker", "kubernetes", "nlp", "computer vision", "scikit-learn"],
        "analyst": ["sql", "excel", "tableau", "powerbi", "data analysis", "reporting", "statistics", "python", "r", "dashboard", "business intelligence", "metrics", "kpi"],
        "devops": ["aws", "azure", "gcp", "linux", "docker", "kubernetes", "ci/cd", "jenkins", "terraform", "ansible", "bash", "python", "scripting", "monitoring", "networking", "cloud"],
        "cloud-arch": ["aws", "azure", "gcp", "architecture", "microservices", "serverless", "networking", "security", "scalability", "load balancing", "terraform", "kubernetes", "cloudnative"],
        "sec-analyst": ["security", "network", "firewall", "vulnerability assessment", "siem", "incident response", "risk management", "wireshark", "snort", "penetration testing", "cybersecurity", "compliance"],
        "pen-tester": ["kali linux", "metasploit", "burp suite", "nmap", "penetration testing", "ethical hacking", "vulnerability", "exploit", "web security", "network security", "owasp", "cryptography"],
        "pm": ["agile", "scrum", "product roadmap", "user stories", "jira", "confluence", "stakeholder management", "data-driven", "market research", "kpi", "leadership", "cross-functional"],
        "scrum": ["agile", "scrum", "kanban", "sprint planning", "retrospectives", "facilitation", "jira", "coach", "impediment", "velocity", "servant leader", "scrum master"],
        "default": [
            "python", "machine learning", "data science", "internship", "project",
            "sql", "communication", "react", "node", "java", "c++", "javascript",
            "html", "css", "mongodb", "express", "aws", "azure", "docker",
            "kubernetes", "leadership", "agile", "rest", "api"
        ]
    }

    keywords = role_keywords.get(role, role_keywords["default"])

    # Score calculation algorithm based on role dataset length
    total_keywords = len(keywords)
    found_keywords_count = sum(1 for word in keywords if word.lower() in text.lower())
    
    # Calculate percentage based on max possible score for this specific role
    resume_score = 0
    if total_keywords > 0:
         resume_score = min(round((found_keywords_count / 10) * 100, 2), 100) # Base goal is hitting 10 keywords for 100%

    if resume_score < 40:
        suggestion = f"Very low ATS match for {role.replace('-', ' ').title()}. Add more role-specific technical keywords and quantify achievements."
    elif resume_score < 70:
        suggestion = f"Good start, but missing some core skills for {role.replace('-', ' ').title()}. Ensure you have listed all your tech stack clearly."
    else:
        suggestion = f"Strong {role.replace('-', ' ').title()} resume! Highlight your project impacts to improve further."

    return {
        "resume_score_percentage": resume_score,
        "suggestion": suggestion
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)
