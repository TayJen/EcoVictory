# ClearNutritionExpert

## Сервис для определения пищевых добавок

## Идея

Создать сервис для определения вредных пищевых добавок в составе продуктов питания и выдаче рекомендаций по употреблению здоровой пищи

## Описание кейса

### Что делает наш бот?

1. Выявляет в составе все пищевые добавки.
2. Предупреждает пользователей о добавках высокой и средней опасности.
3. Дает рекомендации по употреблению продуктов питания

### Какие проблемы существуют?

1. Длинные составы продуктов питания, в которых сложно разобраться.
2. Добавки могут ухудшать состояние человека с определенным заболеванием.
3. Несвоевременное отслеживание исследований по теме.

### Решение проблем

1. Актуальные источники достоверных данных о пищевых добавках.
2. Возможность расшифровать состав конкретного продукта.
3. Возможность узнать о противопоказаниях конкретной добавки
4. Регулярное отслеживание актуальных исследований и изменений

## Запуск бота

Бот открывается по ссылке и запускается нажатием кнопки *"start"*. Также дополнительно можно узнать зачем бот по команде *"help".* Или просто написать боту *"Привет".*

### Схема работы

* После нажатия кнопки *"start"* пользователь может скинуть фотографию состава продукта боту, либо же сразу задать вопрос об интересующей его пищевой добавке.
* Загруженная пользователем фотография обрабатывается моделью OCR, после чего идет суммаризация всех пищевых добавок с помощью ChatGPT Api.

## Демо работы OCR

### Оригинальное изображение состава продукта
![image](https://github.com/TayJen/EcoVictory/assets/57452942/80e72eea-67a4-4ded-a4a0-b73c4026b4c3)

### Детекция текста на изображении
![image](https://github.com/TayJen/EcoVictory/assets/57452942/c8f8b5e3-46ce-42dc-95a7-ba72461f0885)

### Текст с картинки
консервы натуральные горошек из мозговых сортов зеленый стерилизованный высший сорт гост р 54050-2о10 состав горошек зеленый вода питьевая сахар-песок соль поваренная пищевая обьем 425 мл масса нетто 420 г  3 масса основного продукта не менее 252 г изготовитель ооо славянский консервный комбинат россия 353560 краснодарский край славянск-на-кубани ул гриня 5 мы ждем ваши пожелания и замечания по адресу ооо лента россия 197374  санкт-петербург ул савушкина 112 private abel@lentacom продукт готов к употреблению срок годности 4 года дата изготовления указана на крышке банки пищевая ценность 420 г в 100 г продукта белки 31г углеводы 65 г  жиры 0 г витамины в-каротин 03 мг  в1 011мг с 100 мг  минеральные м9 210 мг  вещества р 620 мг  fe 07мг  энергетическая ценность 384 ккал10о г 

