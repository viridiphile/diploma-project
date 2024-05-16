import cv2
from PIL import Image
import logging
from util import get_limits
from colours import colours

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

cap = cv2.VideoCapture(0)
logging.info("Video capture started")

while True:
    ret, frame = cap.read()
    if not ret:
        logging.warning("Failed to capture frame")
        break

    hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    for color_name, bgr_value in colours.items():
        lowerLimit, upperLimit = get_limits(color=bgr_value)
        mask = cv2.inRange(hsvImage, lowerLimit, upperLimit)
        mask_ = Image.fromarray(mask)
        bbox = mask_.getbbox()

        if bbox is not None:
            x1, y1, x2, y2 = bbox
            frame = cv2.rectangle(frame, (x1, y1), (x2, y2), bgr_value, 5)
            cv2.putText(frame, color_name, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, bgr_value, 2)
            logging.info(f"Detected {color_name} color at coordinates: {(x1, y1, x2, y2)}")

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        logging.info("Quitting program")
        break

cap.release()
cv2.destroyAllWindows()
logging.info("Video capture released and windows destroyed")
