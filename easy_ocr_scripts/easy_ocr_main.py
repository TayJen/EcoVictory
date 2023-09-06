import easyocr
import numpy as np


class EasyOcrReader:
    def __init__(self):
        self.reader = easyocr.Reader(['ru'])

    def process_image(self, img_path: str):
        bounds = self.reader.readtext(img_path, paragraph=True)
        answer = self.postprocess(bounds)
        return answer

    def postprocess(self, bounds):
        main_ingredient_list = bounds[0][1]
        
        return main_ingredient_list
