from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator
import cv2
from contextlib import redirect_stdout
import os



def count_people():
    cap = cv2.VideoCapture(1)
    cap.set(3, 640)
    cap.set(4, 480)
    _, img = cap.read()
    model = YOLO('yolov8n.pt')
    results = model.predict(img)
    num_people = 0
    
    with open(os.devnull, 'w') as fnull:
        with redirect_stdout(fnull):
            results = model.predict(img)

    for r in results:
        boxes = r.boxes
        for box in boxes:
            label = model.names[int(box.cls)]
            if label == 'person':
                num_people += 1
    cap.release()
    cv2.destroyAllWindows()

    return num_people

