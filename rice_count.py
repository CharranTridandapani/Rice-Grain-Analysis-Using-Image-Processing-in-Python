import time
import torch
import cv2
import numpy as np

# Load YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'custom',r'C:\Users\Abc\PycharmProjects\pythonProject\yolov5\runs\train\exp2\weights\best.pt')

# Set confidence threshold
conf_threshold = 0.8

# Open video file
cap = cv2.VideoCapture('charran.avi')

# Initialize output video writer
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
out = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc('M','J','P','G'), 30, (frame_width,frame_height))

# Loop over frames in video
while True:
    # Read frame
    ret, frame = cap.read()
    if not ret:
        break

    # Resize frame
    frame = cv2.resize(frame, (640, 480))

    # Convert BGR to RGB and run detection with YOLOv5
    img = frame[:, :, ::-1]
    results = model(img)

    # Draw boxes and display count on each grain
    count = 0
    for i, obj in enumerate(results.xyxy[0]):
        if obj[5] == 0 and obj[4] >= conf_threshold:  # Class index 0 corresponds to rice grains in YOLOv5
            x1, y1, x2, y2 = map(int, obj[:4])
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            count += 1
            cv2.putText(frame, str(count), (x1, y1-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    # Display total count on frame
    cv2.putText(frame, f"Total Count: {count}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Write frame to output video
    out.write(frame)

    # Display frame
    cv2.imshow("result", frame)
    if cv2.waitKey(1) == ord('q'):
        break

# Release video file, output video writer, and destroy windows
cap.release()
out.release()
cv2.destroyAllWindows()
