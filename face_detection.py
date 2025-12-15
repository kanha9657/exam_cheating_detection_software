import cv2
import mediapipe as mp
from datetime import datetime

mp_face = mp.solutions.face_detection
face_detection = mp_face.FaceDetection()

on = cv2.VideoCapture(0)
miss=0
violated=0
violation=[]
while True:
    ret, frame = on.read()
    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_detection.process(rgb)
    if not results.detections:
        miss +=1
    else:
        miss=0
    if miss>5:
        cv2.putText(frame,"Face Not Detected.!",(20,80),cv2.FONT_HERSHEY_SIMPLEX,1,(0, 0, 255),
        3)
    facec = 0

    if results.detections:
        facec = len(results.detections)

    if facec > 1:
        cv2.putText(frame, "MULTIPLE FACES DETECTED!", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
    if facec > 1 or miss > 5:
        if not violation_active:
            violated += 1
            violation_active = True
            time_now = datetime.now().strftime("%H:%M:%S")
            violation.append(time_now)
    else:
        violation_active = False

    cv2.putText(frame,f"violation count ={violated}",(20,40),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,225),3)

    if results.detections:
        for detection in results.detections:
            bbox = detection.location_data.relative_bounding_box
            h, w, _ = frame.shape
            x = int(bbox.xmin * w)
            y = int(bbox.ymin * h)
            width = int(bbox.width * w)
            height = int(bbox.height * h)

            cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 255, 0), 2)

    cv2.imshow("Face Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

on.release()
cv2.destroyAllWindows()
with open("exam_report.txt", "w") as file:
    file.write("AI Exam Cheating Detection Report\n")
    file.write("---------------------------------\n")
    file.write(f"Total Violations: {violated}\n\n")

    for i, time in enumerate(violation, start=1):
        file.write(f"Violation {i} at {time}\n")

print("Exam report generated: exam_report.txt")