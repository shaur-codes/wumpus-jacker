import time
import json
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import cv2
import numpy as np
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='main.log', filemode='w')
logger = logging.getLogger(__name__)

qr_folder = Path("qr_code")
qr_folder.mkdir(exist_ok=True)
cookies_file = Path("discord_cookies.json")

chrome_options = Options()
chrome_options.add_argument("--window-size=1200,800")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--log-level=3") 

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://discord.com/login")

detector = cv2.QRCodeDetector()

def capture_qr_code():
    try:
        qr_element = driver.find_element("tag name", "canvas")
        qr_path = str(qr_folder / "qr_full.png")
        qr_element.screenshot(qr_path)
        logger.info("QR code captured successfully")
        
        img = cv2.imread(qr_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        edges = cv2.Canny(thresh, 50, 200)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        qr_contour = None
        max_area = 0
        for contour in contours:
            approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
            if len(approx) == 4:  # for a sqaure like shape
                area = cv2.contourArea(contour)
                if area > max_area:
                    max_area = area
                    qr_contour = approx

        if qr_contour is not None:
            x, y, w, h = cv2.boundingRect(qr_contour)
            qr_cropped = img[y:y+h, x:x+w]
            qr_cropped_path = str(qr_folder / "qr.png")
            cv2.imwrite(qr_cropped_path, qr_cropped)
            logger.info(f"Cropped QR code saved at: {qr_cropped_path}")
            data, _, _ = detector.detectAndDecode(qr_cropped)
            if data:
                return True, max_area  # QR code detected with its area
            else:
                return False, max_area  # Square detected but not a QR code
        else:
            logger.warning("No square contour detected")
            return False, 0 

    except Exception as e:
        logger.error(f"Error capturing QR code: {str(e)}")
        return False, 0

def export_cookies():
    cookies = driver.get_cookies()
    with open(cookies_file, "w") as file:
        json.dump(cookies, file)
    logger.info(f"Cookies exported to {cookies_file}")

try:
    initial_area = None

    while True:
        qr_detected, current_area = capture_qr_code()
        if qr_detected and initial_area is None:
            initial_area = current_area  # Set baseline QR code area
            logger.info(f"Initial QR code area set: {initial_area}")
        elif initial_area is not None:
            if not qr_detected or abs(current_area - initial_area) > 0.2 * initial_area:
                # QR code disappeared or largest square changed significantly
                logger.info("QR code scan detected, login successful")
                export_cookies()
                with open("login_success.txt", "w") as f:
                    f.write("login successful")
                
        time.sleep(2)

except KeyboardInterrupt:
    logger.info("Monitoring stopped by user")
finally:
    driver.quit()
