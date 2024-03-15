Приложение для диагноза церроза печени методами ML

Доступно 3 модели -- desition tree (5 coins), KNN (10 coins), boosting (15 coins)

## Запуск

Python == 3.8 

pip install -r requriments.txt

sudo python3 main.py в папке app

Заходить на localhost:81

## Приложение 

![изображение](https://github.com/KozhevnikovAlexandr/ML_practicum/assets/56560126/a4ea8b51-b307-4e20-886e-f1fcf0ecd679)

![изображение](https://github.com/KozhevnikovAlexandr/ML_practicum/assets/56560126/6fb49a79-07b3-4c6c-a205-4b8f2c362848)


## API 

Swagger -- http://localhost:81/docs#/

POST /resiter - регистрирует юзера в базе 
POST /login - возвращает токен по емейлу и паролю 
POST /predict - в заголовке токен, в теле запроса данные для модели 

## БД 
