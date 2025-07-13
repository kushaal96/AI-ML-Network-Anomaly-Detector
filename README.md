# Network Anomaly Detection

This project detects anomalies in network traffic using machine learning. It includes:
- 🧠 A Python backend for model inference and data processing
- 🌐 A ReactJS frontend for live monitoring and visualization

---

## 📦 Project Structure

ai-ml/
├── app.py # Backend server (Flask or FastAPI)
├── network-monitor/ # React frontend
├── *.py # Various preprocessing & model scripts
├── *.pkl # Trained models
├── *.xlsx / *.csv # Sample data
└── .gitignore, README.md

yaml
Copy
Edit

---

## 🚀 Getting Started

### 1. Backend (Python)
Navigate to the project root:

```bash
cd ai-ml
pip install -r requirements.txt
python app.py
This will start your backend server.

2. Frontend (React)
bash
Copy
Edit
cd ai-ml/network-monitor
npm install
npm start
This will launch the React app on http://localhost:3000

🔧 Requirements
Python 3.x

Node.js (for frontend)

Packages: listed in requirements.txt (run pip freeze > requirements.txt)

