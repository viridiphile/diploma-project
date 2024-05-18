import cv2
from PIL import Image
import logging
from util import get_limits, load_config
from colours import colours
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load configuration
config = load_config()

cap = cv2.VideoCapture(0)
logging.info("Video capture started")

kernel_size = config.get("kernel_size", 5)
min_contour_area = config.get("min_contour_area", 1000)
kernel = np.ones((kernel_size, kernel_size), np.uint8)

while True:
    ret, frame = cap.read()
    if not ret:
        logging.warning("Failed to capture frame")
        break

    hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    for color_name, bgr_value in colours.items():
        lowerLimit, upperLimit = get_limits(color=bgr_value, config=config)
        mask = cv2.inRange(hsvImage, lowerLimit, upperLimit)

        # Apply morphological operations
        mask = cv2.erode(mask, kernel, iterations=1)
        mask = cv2.dilate(mask, kernel, iterations=1)

        # Find contours and filter by area
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > min_contour_area:  # Filter out small areas
                x, y, w, h = cv2.boundingRect(contour)
                frame = cv2.rectangle(frame, (x, y), (x + w, y + h), bgr_value, 5)
                cv2.putText(frame, color_name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, bgr_value, 2)
                logging.info(f"Detected {color_name} color at coordinates: {(x, y, x + w, y + h)}")

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        logging.info("Quitting program")
        break

cap.release()
cv2.destroyAllWindows()
logging.info("Video capture released and windows destroyed")
