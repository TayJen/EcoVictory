import openai
from pathlib import Path
import json
import os
from typing import List, Dict


BASE_DIR = Path(__file__).resolve().parent.parent

MAX_HISTORY_SIZE = 15

START_PROMPT = '''
You will be acting as an expert in nutrition and healthy eating habits. Your mission is to create a comprehensive guide on how to make healthy meal plans that cater to different dietary needs and preferences. Your guide should include step-by-step instructions, sample meal plans, and a list of foods to include and avoid for each diet.

To begin, please introduce yourself by typing "Hi, I am a nutrition expert."

You will need to first research and understand the different dietary needs and preferences such as vegetarian, vegan, paleo, ketogenic, etc. Then, you will create a list of foods that are suitable for each dietary preference along with their nutritional value. You will also need to provide suggestions for substitutes for any food items that may not be available in certain regions.

Once you have a good understanding of the different dietary preferences, you will then start creating sample meal plans for each preference. Your meal plans should include breakfast, lunch, dinner, and snack options. You should also include the number of servings and the amount of each food item to be consumed.

To make your guide more engaging, you can add tips on how to make the meal plans more interesting, how to meal prep, and how to make healthier choices when dining out. You can also include some of your favorite recipes and cooking techniques.

Throughout the guide, please use concise and clear language that is easy to follow. Use headings, bullet points, and other formatting techniques to make the guide more visually appealing and easier to read.

Please ask for clarification or additional information as needed, and provide updates on your progress. Remember, you are an expert in nutrition and healthy eating habits, and are expected to use best practices in creating this guide. Good luck, and happy planning!

You don't need to say hello for each prompt, act like it is infinite dialogue. You also need to answer only in Russian language.
'''

class ChatGPTExpert:
    def __init__(self, api_key: str, model_name: str):
        openai.api_key = api_key
        self.model_name = model_name
        self.ingredient_prompt = "Найди все добавки E, ароматизаторы, консерванты, усилители вкуса, лецитины в составе продукта. Состав продукта:"
        self.ingredient_prompt_end = "Выдели из состава пищевые добавки, разбей их по типу(группам).\n" + \
            "Расскажи вреден ли он для здоровья человека? Могут ли быть какие либо противопоказания по имеющимся добавкам?"
        self.base_start_history = [{"role": "user", "content": START_PROMPT}, 
                                   {"role": "assistant", "content": "OK"}]

    def preprocess_prompt(self, raw_prompt: str) -> str:
        processed_prompt = raw_prompt + " Отвечай на русском языке, и с описанием побочных эффектов и возможных последствий, если вопрос про пищевую добавку"
        return processed_prompt

    def get_user_history(self, user_id: int) -> List[Dict[str, str]]:
        """
            Gets user history of conversation for the specified user.
            If there is no, then just the START_PROMPT
        """
        with open(os.path.join(BASE_DIR, "data/users_message_histories.json"), "r") as json_history_file:
            all_history = json.load(json_history_file)
            # If user didn't chat before, there will be a start prompt
            if user_id not in all_history:
                user_history = self.base_start_history.copy()
            else:
                user_history = all_history[user_id]
                # If user chatted too much, then the history will be reset to the start prompt
                if len(user_history) > MAX_HISTORY_SIZE:
                    user_history = self.base_start_history.copy()   # Reset history if it is greater than limit

        return all_history, user_history

    def resave_user_history(self, all_history: Dict[int, List[Dict[str, str]]]) -> None:
        with open(os.path.join(BASE_DIR, "data/users_message_histories.json"), "w") as json_history_file:
            json.dump(all_history, json_history_file)


    def get_message_answer_user(self, user_id: int, user_prompt: str) -> str:
        """
            For given user_id and user_prompt generates prompt, if user is not in history yet, then
            he has a start prompt for GPT Nutrition Expert.

            :param user_id: int, id of the telegram user
            :param iser_prompt: string, users prompt to the model
            :return: string, answer to the prompt from GPT Nutrition Expert
        """
        print(f"User_ID: {user_id}")

        # Get all users history and specific user_id history
        all_history, user_history = self.get_user_history(user_id)
        print(f"User History: {user_history}")

        # Process prompt and add it to the users history
        processed_prompt = self.preprocess_prompt(user_prompt)
        user_history.append({"role": "user", "content": f"{processed_prompt}"})
        print(processed_prompt)

        # Get answer using openai API
        completion = openai.ChatCompletion.create(
            model=self.model_name,   # this is "ChatGPT" $0.002 per 1k tokens
            messages=user_history
        )

        # Get reply from dict completion and add it to the users history
        reply_content = completion.choices[0].message.content
        user_history.append({"role": "assistant", "content": f"{reply_content}"})
        print(user_id, reply_content)

        # Resave the all users histories json
        all_history[user_id] = user_history
        self.resave_user_history(all_history)

        return reply_content

    def get_message_answer_ingredients(self, ingredient_list: str, user_id: int):
        """
            Get message for our own ingredients findings, here find E additives in ingredient list

            :param ingredient_list: string, list of ingredients in the product
            :param user_id: int, id of the user, to track history of his prompts
        """
        prompt = self.ingredient_prompt + '\n' + ingredient_list + '\n' + self.ingredient_prompt_end
        print(prompt)

        # Get all users history and specific user_id history
        all_history, user_history = self.get_user_history(user_id)
        print(f"User History: {user_history}")

        user_history.append({"role": "user", "content": f"{prompt}"})

        # Get answer using openai API
        completion = openai.ChatCompletion.create(
            model=self.model_name,   # this is "ChatGPT" $0.002 per 1k tokens
            messages=[{"role": "user", "content": prompt}]
        )

        # Get reply from dict completion and add it to the users history
        reply_content = completion.choices[0].message.content
        user_history.append({"role": "assistant", "content": f"{reply_content}"})

        # Resave the all users histories json
        all_history[user_id] = user_history
        self.resave_user_history(all_history)

        return reply_content


if __name__ == "__main__":
    print(BASE_DIR)