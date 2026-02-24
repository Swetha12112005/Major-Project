
document.getElementById("predictionForm").addEventListener("submit", async function(e) {
    e.preventDefault();

    const data = {
        cgpa: parseFloat(document.getElementById("cgpa").value),
        internships: parseInt(document.getElementById("internships").value),
        projects: parseInt(document.getElementById("projects").value),
        aptitude_score: parseFloat(document.getElementById("aptitude_score").value),
        communication_score: parseFloat(document.getElementById("communication_score").value)
    };

    const response = await fetch("http://127.0.0.1:8000/predict", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(data)
    });

    const result = await response.json();
    document.getElementById("result").innerText =
        "Placement Probability: " + result.placement_probability;
});

document.getElementById("resumeForm").addEventListener("submit", async function(e) {
    e.preventDefault();

    const fileInput = document.getElementById("resumeFile");
    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    const response = await fetch("http://127.0.0.1:8000/resume-analyzer", {
        method: "POST",
        body: formData
    });

    const result = await response.json();
    document.getElementById("resumeResult").innerText =
        "Resume Score: " + result.resume_score_percentage + "%";
});
