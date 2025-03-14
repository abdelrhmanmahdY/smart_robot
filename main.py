from config import *
from motor import *
from time import sleep
import cv2
import threading
from gpiozero import Motor
from picamera2 import Picamera2
from ultralytics import YOLO

# Initialize motor control (adjust GPIO pins as needed)
motor = Motor(forward=motor1_en4, backward=motor1_en4)



# Set up the camera with Picam
picam2 = Picamera2()
picam2.preview_configuration.main.size = (1280, 1280)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()

model = YOLO("yolov5n.pt")

while True:
    frame = picam2.capture_array()
    results = model(frame, classes=[0])

    # Check if any person is detected
    if results[0].boxes:
        threading.Thread(target=move(forward=True,motor=motor), daemon=True).start()  # Move motor in a separate thread
    else:
        stop(motor)  
    annotated_frame = results[0].plot()
    inference_time = results[0].speed['inference']
    fps = 1000 / inference_time  # Convert to milliseconds
    text = f'FPS: {fps:.1f}'
    font = cv2.FONT_HERSHEY_SIMPLEX
    text_size = cv2.getTextSize(text, font, 1, 2)[0]
    text_x = annotated_frame.shape[1] - text_size[0] - 10
    text_y = text_size[1] + 10
    cv2.putText(annotated_frame, text, (text_x, text_y), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.imshow("Camera", annotated_frame)

 
    if cv2.waitKey(1) == ord("q"):
        break

cv2.destroyAllWindows()
