🚦 Real-Time AI Traffic Monitoring System

An AI-powered traffic monitoring application designed to detect vehicles, monitor traffic density, and identify potential restricted-lane violations using computer vision.

✨ Features

- 🚗 Real-time vehicle detection
- 🏍️ Car, motorcycle, bus, and truck classification
- 📊 Vehicle counting and traffic density estimation
- 🚨 Basic restricted-lane violation detection
- 🎥 Webcam video processing
- ⚡ Real-time communication using WebSockets
- 📈 Interactive React dashboard
- 💾 SQLite database for traffic events

🛠️ Tech Stack

Frontend: React.js, Vite, CSS
Backend: Python, FastAPI
AI/Computer Vision: YOLO11, OpenCV
Database: SQLite
Communication: WebSockets

🏗️ Architecture

Webcam
   ↓
React Frontend
   ↓
WebSocket Connection
   ↓
FastAPI Backend
   ↓
YOLO Vehicle Detection
   ↓
OpenCV Processing
   ↓
Traffic Statistics & Alerts
   ↓
Dashboard

📁 Project Structure

real_time_traffic_monitoring/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── detector.py
│   │   ├── database.py
│   │   └── __init__.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── style.css
│   ├── package.json
│   └── index.html
└── README.md

⚙️ Installation and Setup

Prerequisites

- Python 3.10 or newer
- Node.js and npm
- Visual Studio Code
- A webcam

1. Clone the repository

git clone YOUR_GITHUB_REPOSITORY_URL
cd real_time_traffic_monitoring

Replace "YOUR_GITHUB_REPOSITORY_URL" with your repository's actual URL.

2. Set up the backend

cd backend
python -m venv venv

On Windows:

venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Start the backend:

uvicorn app.main:app --reload

Backend API: http://127.0.0.1:8000

API documentation: http://127.0.0.1:8000/docs

3. Set up the frontend

Open a second terminal in VS Code:

cd frontend
npm install
npm run dev

Open the local URL printed by Vite, usually http://localhost:5173.

Allow webcam access when prompted, then click Start Monitoring.

🚀 Future Improvements

- Vehicle tracking with unique IDs
- More accurate lane detection
- Calibrated vehicle speed estimation
- Number-plate recognition
- User authentication and role-based access
- PostgreSQL integration
- Traffic analytics and historical reports
- Deployment to a cloud platform

⚠️ Limitations

This project is an educational prototype. Lane violations are estimated using a simple image-region rule and do not establish actual legal violations. Accurate speed measurement requires camera calibration. Detection performance depends on camera quality, lighting, and hardware.

📄 License

This project is distributed under the MIT License, subject to the repository's license file.

👨‍💻 Author

Developed as an AI, computer vision, and full-stack development portfolio project.
