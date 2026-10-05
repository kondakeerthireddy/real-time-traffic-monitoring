import base64
import cv2
import numpy as np

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .detector import TrafficDetector
from .database import SessionLocal, TrafficEvent

app = FastAPI(title="Real-Time AI Traffic Monitoring API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

detector = TrafficDetector()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "Traffic Monitoring API", "status": "running"}

@app.get("/api/health")
def health():
    return {"status": "healthy"}

@app.get("/api/events")
def events(limit: int = 50, db: Session = Depends(get_db)):
    rows = db.query(TrafficEvent).order_by(
        TrafficEvent.id.desc()
    ).limit(limit).all()

    return [
        {
            "id": r.id,
            "vehicle_type": r.vehicle_type,
            "confidence": r.confidence,
            "violation": r.violation,
            "created_at": r.created_at.isoformat()
        }
        for r in rows
    ]

@app.websocket("/ws/traffic")
async def traffic_socket(ws: WebSocket):
    await ws.accept()

    try:
        while True:
            message = await ws.receive_text()
            payload = message.split(",", 1)[-1]

            frame = cv2.imdecode(
                np.frombuffer(
                    base64.b64decode(payload),
                    dtype=np.uint8
                ),
                cv2.IMREAD_COLOR
            )

            if frame is None:
                continue

            annotated, stats = detector.process(frame)

            if stats["violations"] > 0:
                db = SessionLocal()
                try:
                    db.add(TrafficEvent(
                        vehicle_type="vehicle",
                        confidence=0.0,
                        violation="restricted_lane"
                    ))
                    db.commit()
                finally:
                    db.close()

            ok, encoded = cv2.imencode(
                ".jpg", annotated,
                [int(cv2.IMWRITE_JPEG_QUALITY), 70]
            )

            if not ok:
                continue

            image = base64.b64encode(encoded.tobytes()).decode()

            await ws.send_json({
                "image": image,
                "stats": stats
            })

    except WebSocketDisconnect:
        print("Client disconnected")
