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
        main_ingredient_list = ""
        for bound in bounds:
            main_ingredient_list += bound[1].lower() + ' '

        # Remove unnecessary punctuation and other symbols
        unnecessary_symbols = ";:.,!?%#\"'/\\"
        for sym in unnecessary_symbols:
            main_ingredient_list = main_ingredient_list.replace(sym, '')

        # Remove extra spaces
        main_ingredient_list = " ".join(main_ingredient_list.split(' '))

        return main_ingredient_list
