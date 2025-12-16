import cv2
import mediapipe as mp
from datetime import datetime

# MediaPipe face detection
mp_face = mp.solutions.face_detection
face_detection = mp_face.FaceDetection(min_detection_confidence=0.5)

# Webcam
cam = cv2.VideoCapture(0)

# Variables
miss = 0
violated = 0
violation = []
violation_active = False

while True:
    ret, frame = cam.read()
    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_detection.process(rgb)

    # Face count
    facec = len(results.detections) if results.detections else 0

    # Face missing logic
    if facec == 0:
        miss += 1
    else:
        miss = 0

    # ===== VIOLATION LOGIC =====
    if facec > 1 or miss > 5:
        if not violation_active:
            violated += 1
            violation_active = True
            time_now = datetime.now().strftime("%H:%M:%S")
            violation.append(time_now)
    else:
        violation_active = False

    # ===== DISPLAY TEXT (NO OVERLAP) =====
    cv2.putText(frame, f"Violation Count: {violated}",
                (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

    if facec > 1:
        cv2.putText(frame, "MULTIPLE FACES DETECTED!",
                    (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

    if miss > 5:
        cv2.putText(frame, "FACE NOT DETECTED!",
                    (20, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

    # Draw face boxes
    if results.detections:
        for detection in results.detections:
            bbox = detection.location_data.relative_bounding_box
            h, w, _ = frame.shape
            x = int(bbox.xmin * w)
            y = int(bbox.ymin * h)
            bw = int(bbox.width * w)
            bh = int(bbox.height * h)

            cv2.rectangle(frame, (x, y), (x + bw, y + bh), (0, 255, 0), 2)

    cv2.imshow("AI Exam Proctoring System", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()

# ===== REPORT GENERATION =====
with open("exam_report.txt", "w") as file:
    file.write("AI Exam Cheating Detection Report\n")
    file.write("---------------------------------\n")
    file.write(f"Total Violations: {violated}\n\n")
    for i, t in enumerate(violation, start=1):
        file.write(f"Violation {i} at {t}\n")

print("Exam report generated: exam_report.txt")
