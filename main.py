import Constants as keys
from telegram.ext import *
import Responses as R
import cv2
# from keras.models import load_model
import numpy as np
from io import BytesIO
from easy_ocr_scripts.easy_ocr_main import EasyOcrReader


print('Bot started...')


def start_command(update, context):
    update.message.reply_text(f'Hello {update.message.from_user.first_name}!')


def help_command(update, context):
    update.message.reply_text('Просто отправь фото cостава продукта;)')


def handle_message(update, context):
    text = str(update.message.text).lower()
    response = R.sample_responses(text)

    update.message.reply_text(response)


def get_image(update, context, ocr_reader=EasyOcrReader()):
    photo = update.message.photo[-1].get_file()

    random_number = np.random.randint(500000)
    img_path = f'images/img_{random_number}.jpg'
    photo.download(img_path)

    # https://stackoverflow.com/questions/59876271/how-to-process-images-from-telegram-bot-without-saving-to-file
    # img = cv2.imread(photo)
    # img = cv2.imdecode(np.fromstring(BytesIO(photo.download_as_bytearray()).getvalue(), np.uint8), 1)

    # pred = model.predict(img)
    answer = ocr_reader.process_image(img_path)
    print(answer)

    response = answer
    update.message.reply_text(response)


def error(update, context):
    print(f'Update {update} caused error: {context.error}')


def main():
    updater = Updater(keys.API_KEY, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start_command))
    dp.add_handler(CommandHandler('help', help_command))

    dp.add_handler(MessageHandler(Filters.text, handle_message))
    dp.add_handler(MessageHandler(Filters.photo, get_image))
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


main()
