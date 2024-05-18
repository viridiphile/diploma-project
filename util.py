import numpy as np
import cv2
import json

def load_config(config_file="config.json"):
    with open(config_file, 'r') as f:
        config = json.load(f)
    return config

config = load_config()

def get_limits(color, config=config):
    c = np.uint8([[color]])  # BGR values
    hsvC = cv2.cvtColor(c, cv2.COLOR_BGR2HSV)

    hue = hsvC[0][0][0]  # Get the hue value
    hue_range = config["hue_range"]
    sat_min = config["saturation_min"]
    sat_max = config["saturation_max"]
    val_min = config["value_min"]
    val_max = config["value_max"]

    # Handle red hue wrap-around
    if hue >= 165:  # Upper limit for divided red hue
        lowerLimit = np.array([hue - hue_range, sat_min, val_min], dtype=np.uint8)
        upperLimit = np.array([180, sat_max, val_max], dtype=np.uint8)
    elif hue <= 15:  # Lower limit for divided red hue
        lowerLimit = np.array([0, sat_min, val_min], dtype=np.uint8)
        upperLimit = np.array([hue + hue_range, sat_max, val_max], dtype=np.uint8)
        return lowerLimit, upperLimit

    lowerLimit = np.array([hue - hue_range, sat_min, val_min], dtype=np.uint8)
    upperLimit = np.array([hue + hue_range, sat_max, val_max], dtype=np.uint8)

    return lowerLimit, upperLimit
