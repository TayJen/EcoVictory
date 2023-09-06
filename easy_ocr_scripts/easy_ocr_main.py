import easyocr
import numpy as np


class EasyOcrReader:
    def __init__(self):
        self.reader = easyocr.Reader(['ru'])

    def process_image(self, img_path: str):
        bounds = self.reader.readtext(img_path)
        answer = self.postprocess(bounds)
        return answer

    def postprocess(self, bounds):
        return bounds
