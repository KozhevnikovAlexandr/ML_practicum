Приложение для диагноза церроза печени методами ML

Доступно 3 модели -- desition tree (5 coins), KNN (10 coins), boosting (15 coins)

Пользователь регистрируется, получает 100 моент. Заполняет форму где выбирает модель и вводит параметры. Получает ответ. За использование монеты снимаеются.

Можно работать как через веб, так и через API

Для аутентификации используется accsess_token, который возвращается при логине.

Результаты записываются в базу, схема базы ниже.

## Запуск

Python == 3.8 

pip install -r requriments.txt

sudo python3 main.py в папке app

Заходить на localhost:81

## Пример данных 

{
  "ModelName": "boosting",
  "N_Days": 400,
  "Drug": "D-penicillamine",
  "Age": 21464,
  "Sex": "F",
  "Ascites": "Y",
  "Hepatomegaly": "Y",
  "Spiders": "Y",
  "Edema": "Y",
  "Bilirubin": 14.5,
  "Cholesterol": 261.0,
  "Albumin": 2.6,
  "Copper": 156.0,
  "Alk_Phos": 1718.0,
  "SGOT": 137.95,
  "Tryglicerides": 172.0,
  "Platelets": 190.0,
  "Prothrombin": 12.2,
  "Stage": 4.0
}

## Приложение 

![изображение](https://github.com/KozhevnikovAlexandr/ML_practicum/assets/56560126/a4ea8b51-b307-4e20-886e-f1fcf0ecd679)

![изображение](https://github.com/KozhevnikovAlexandr/ML_practicum/assets/56560126/6fb49a79-07b3-4c6c-a205-4b8f2c362848)


## API 

Swagger -- http://localhost:81/docs#/

POST /resiter - регистрирует юзера в базе 

POST /login - возвращает токен по емейлу и паролю 

POST /predict - в заголовке токен, в теле запроса данные для модели 

## БД 

![изображение](https://github.com/KozhevnikovAlexandr/ML_practicum/assets/56560126/e01a2189-7f8d-4916-ba82-4a2b070d37b7)


