import os

import cv2
import numpy as np
import Responses as R
from dotenv import load_dotenv
from telegram import InputTextMessageContent, BotCommand
from telegram.ext import Application, ApplicationBuilder, MessageHandler, CommandHandler, filters

from easy_ocr_scripts.easy_ocr_main import EasyOcrReader
from chatgpt_scripts.chatgpt_main import ChatGPTExpert


class TelegramBot:
    def __init__(self):
        self.application = ApplicationBuilder() \
            .token(os.environ['TELEGRAM_BOT_TOKEN']) \
            .post_init(self.post_init) \
            .concurrent_updates(True) \
            .build()

        self.commands = [
            BotCommand(command='help', description="Описание работы бота"),
            BotCommand(command='start', description="Стартовая команда для началы работы бота"),
        ]
        # self.updater = Updater(os.environ['TELEGRAM_BOT_TOKEN'])
        self.ocr_reader = EasyOcrReader()
        self.gpt_helper = ChatGPTExpert(api_key=os.environ['OPENAI_API_KEY'], model_name=os.environ['OPENAI_MODEL'])

    @staticmethod
    async def start_command(update, context):
        await update.message.reply_text(f"Привет {update.message.from_user.first_name}! " + \
                                        "Я Эксперт по вопросам питания ChatGPT, который также может по твоей фотографии состава разобрать добавки в продукте!")

    @staticmethod
    async def help_command(update, context):
        await update.message.reply_text("Просто отправь фото состава продукта или задай вопрос по интересующему тебя вопросу " + \
                                        "относительно питания и различных добавок")

    async def handle_message(self, update, context):
        text = str(update.message.text).lower()
        response = R.sample_responses(text)
        if not response:
            response = self.gpt_helper.get_message_answer_user(
                user_id=update.message.from_user['id'],
                user_prompt=text
            )

        await update.message.reply_text(response)

    async def get_image(self, update, context):
        random_number = np.random.randint(500000)
        img_path = f'images/img_{random_number}.jpg'

        await (await context.bot.getFile(update.message.photo[-1].file_id)).download_to_drive(img_path)

        ingredients_str = await self.ocr_reader.process_image(img_path)
        response = self.gpt_helper.get_message_answer_ingredients(
            ingredient_list=ingredients_str,
            user_id=update.message.from_user['id']
        )

        await update.message.reply_text(response)

    @staticmethod
    def error(update, context):
        print(f'Update {update} caused error: {context.error}')

    async def post_init(self, application: Application) -> None:
        """
            Post initialization hook for the bot
        """
        await application.bot.set_my_commands(self.commands)

    def start_bot(self):
        self.application.add_handler(CommandHandler('start', self.start_command))
        self.application.add_handler(CommandHandler('help', self.help_command))

        # static_handle_message = lambda update, context: self.handle_message(update, context)
        self.application.add_handler(MessageHandler(filters.TEXT, self.handle_message))

        # static_get_image = lambda update, context: self.get_image(update, context)
        self.application.add_handler(MessageHandler(filters.PHOTO, self.get_image))
        self.application.add_error_handler(self.error)

        self.application.run_polling()


if __name__ == "__main__":
    # Read .env file
    load_dotenv()

    bot = TelegramBot()
    print('Bot initialized')

    bot.start_bot()
    print('Bot ended')
