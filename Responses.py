import json
import pandas as pd


def sample_responses(input_text):
    user_message = str(input_text).lower()

    if user_message in ('hello', 'hi', 'sup', 'привет', 'здравствуй'):
        return "Привет! Просто скинь мне фото состава продуктов!"

    if user_message in ('who are you', 'who are you?', 'кто ты', 'кто ты?'):
        return 'Я EcoVictoryBot, помогаю с определением безопасности продуктов по их составу.  Даю рекомендации по питанию'

    return "Я не понимаю тебя :("


def photo_response(pred):
    df = pd.read_csv('data/Описание .csv')
    with open('data/labels.json', 'r') as fp:
        labels = json.load(fp)
        pred = labels[str(pred)]
        out = df[df['GroupName'] == pred]['Description'].values[0]

    output = pred + '\n' + out

    return output


# print(photo_response(1))



