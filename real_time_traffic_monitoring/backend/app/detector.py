import cv2
from ultralytics import YOLO

VEHICLE_CLASSES = {
    2: "car",
    3: "motorcycle",
    5: "bus",
    7: "truck",
}

class TrafficDetector:
    def __init__(self):
        self.model = YOLO("yolo11n.pt")

    def process(self, frame):
        h, w = frame.shape[:2]
        restricted_x = int(w * 0.75)

        result = self.model.predict(
            frame,
            conf=0.35,
            classes=list(VEHICLE_CLASSES),
            verbose=False
        )[0]

        counts = {v: 0 for v in VEHICLE_CLASSES.values()}
        violations = 0

        cv2.line(frame, (restricted_x, 0), (restricted_x, h), (255,255,0), 2)
        cv2.putText(
            frame, "Restricted lane",
            (restricted_x + 8, 30),
            cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255,255,0), 2
        )

        if result.boxes is not None:
            for box in result.boxes:
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                vehicle = VEHICLE_CLASSES.get(cls_id)
                if not vehicle:
                    continue

                counts[vehicle] += 1
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cx = (x1 + x2) // 2
                violation = cx >= restricted_x

                if violation:
                    violations += 1

                label = f"{vehicle} {conf:.2f}"
                if violation:
                    label += " | VIOLATION"

                color = (0,0,255) if violation else (0,255,0)
                cv2.rectangle(frame, (x1,y1), (x2,y2), color, 2)
                cv2.putText(
                    frame, label, (x1, max(20,y1-8)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, color, 2
                )

        total = sum(counts.values())
        density = "Low" if total == 0 else "Medium" if total <= 5 else "High"

        return frame, {
            "total": total,
            "counts": counts,
            "violations": violations,
            "density": density
        }
