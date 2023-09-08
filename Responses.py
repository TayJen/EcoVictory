def sample_responses(input_text):
    user_message = str(input_text).lower()

    if user_message in ('hello', 'hi', 'sup', 'привет', 'здравствуй'):
        return "Привет! Просто скинь мне фото состава продукта! Либо задавай любой вопрос по питанию и я с радостью тебе на него отвечу!"

    if user_message in ('who are you', 'who are you?', 'кто ты', 'кто ты?'):
        return "Я Эксперт по вопросам питания ChatGPT, помогаю с определением безопасности продуктов по их составу и даю рекомендации по питанию"

    return ""
