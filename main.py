import logging
import os
from io import BytesIO

import cv2
import numpy as np
import Responses as R
from dotenv import load_dotenv
from telegram.ext import *

from easy_ocr_scripts.easy_ocr_main import EasyOcrReader
from chatgpt_scripts.chatgpt_main import ChatGPTExpert


class TelegramBot:
    def __init__(self):
        self.updater = Updater(os.environ['TELEGRAM_BOT_TOKEN'], use_context=True)
        self.ocr_reader = EasyOcrReader()
        self.gpt_helper = ChatGPTExpert()

    @staticmethod
    def start_command(update, context):
        update.message.reply_text(f'Hello {update.message.from_user.first_name}!')

    @staticmethod
    def help_command(update, context):
        update.message.reply_text('Просто отправь фото cостава продукта;)')

    @staticmethod
    def handle_message(update, context):
        text = str(update.message.text).lower()
        response = R.sample_responses(text)

        update.message.reply_text(response)

    @staticmethod
    def get_image(update, context, ocr_reader=EasyOcrReader()):
        photo = update.message.photo[-1].get_file()

        random_number = np.random.randint(500000)
        img_path = f'images/img_{random_number}.jpg'
        photo.download(img_path)

        # https://stackoverflow.com/questions/59876271/how-to-process-images-from-telegram-bot-without-saving-to-file
        # img = cv2.imread(photo)
        # img = cv2.imdecode(np.fromstring(BytesIO(photo.download_as_bytearray()).getvalue(), np.uint8), 1)

        answer = ocr_reader.process_image(img_path)

        response = answer
        update.message.reply_text(response)

    @staticmethod
    def error(update, context):
        print(f'Update {update} caused error: {context.error}')

    def start_bot(self):
        dp = self.updater.dispatcher

        dp.add_handler(CommandHandler('start', self.start_command))
        dp.add_handler(CommandHandler('help', self.help_command))

        dp.add_handler(MessageHandler(Filters.text, self.handle_message))
        dp.add_handler(MessageHandler(Filters.photo, self.get_image))
        dp.add_error_handler(self.error)

        self.updater.start_polling()
        self.updater.idle()


if __name__ == "__main__":
    # Read .env file
    load_dotenv()

    bot = TelegramBot()
    print('Bot initialized')

    bot.start_bot()
    print('Bot started')
