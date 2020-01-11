import cv2
from PIL import Image
import os
import pytesseract
import numpy as np


# Resolves captcha image given in constructor and stores the text in captcha_text attribute
class CaptchaResolver:

    pytesseract.pytesseract.tesseract_cmd = os.path.join(os.getcwd(), r'Tesseract-OCR\tesseract.exe')
    GRAY_SCALE_IMAGE_NAME = 'gray_scale_captcha.png'
    INVERTED_IMAGE_NAME = 'inverted_captcha.png'

    def __init__(self, image_path):

        # Using PIL to open image as captcha image couldn't be opened by cv2.imread for some reason
        self.image = Image.open(image_path)

        self.captcha_text = ''
        self.processed_image = None

    # Converts the image to gray scale as the captcha is in RGB
    def convert_to_gray_scale(self):
        gray_scale_image = self.image.convert('LA')
        gray_scale_image.save(CaptchaResolver.GRAY_SCALE_IMAGE_NAME)

    # Inverting colors because grayscale image yields white text on black background
    def invert_colors(self):
        self.convert_to_gray_scale()
        gray_scale_image = cv2.imread(CaptchaResolver.GRAY_SCALE_IMAGE_NAME)
        cv2.imwrite(CaptchaResolver.INVERTED_IMAGE_NAME, ~gray_scale_image)

    # Performing pre-processing so that captcha can be accurately read
    def preprocess_image(self):
        self.invert_colors()
        self.processed_image = cv2.resize(cv2.imread(CaptchaResolver.INVERTED_IMAGE_NAME), None, fx=1.5, fy=1.5,
                                          interpolation=cv2.INTER_CUBIC)
        self.processed_image = cv2.cvtColor(self.processed_image, cv2.COLOR_BGR2GRAY)
        kernel = np.ones((1, 1), np.uint8)
        self.processed_image = cv2.dilate(self.processed_image, kernel, iterations=1)
        self.processed_image = cv2.erode(self.processed_image, kernel, iterations=1)
        self.processed_image = cv2.medianBlur(self.processed_image, 3)

    def read_captcha(self):
        self.preprocess_image()

        # Since the captcha here contains only numeric characters, we confined the whitelist to numbers
        self.captcha_text = pytesseract.image_to_string(self.processed_image, lang='eng',
                                                        config='--psm 11 --oem 0 -c tessedit_char_whitelist=0123456789')

        # Removing space as OCR always gives a space after 2 or 3 characters i.e 23<space>174
        self.captcha_text = "".join(self.captcha_text.split())
        self.delete_images()

    @staticmethod
    def delete_images():
        try:
            os.remove("gray_scale_captcha.png")
            os.remove("inverted_captcha.png")
        except FileNotFoundError:
            print('File does not exist')
