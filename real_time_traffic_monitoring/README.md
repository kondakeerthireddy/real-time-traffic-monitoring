# Real-Time AI Traffic Monitoring System

Full-stack portfolio project using YOLO, OpenCV, FastAPI, WebSockets, React and SQLite.

## Features
- Live browser webcam
- YOLO vehicle detection
- Car, motorcycle, bus and truck counts
- Traffic density
- Simple restricted-lane violation detection
- WebSocket real-time processing
- Event database
- React dashboard

## Run backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backend: http://127.0.0.1:8000

## Run frontend
Install Node.js 18+.

```bash
cd frontend
npm install
npm run dev
```

Open the Vite URL, normally http://localhost:5173.

The first YOLO inference downloads the model automatically.

## GitHub
```bash
git init
git add .
git commit -m "Initial real-time traffic monitoring system"
git branch -M main
git remote add origin YOUR_REPOSITORY_URL
git push -u origin main
```

This is an educational/portfolio implementation. Speed estimation and number-plate recognition require camera calibration and separate production-grade pipelines.
