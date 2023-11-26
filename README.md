##  Тестовое задание от LeadHit на позицию Junior Python Developer

###  Forms Filled Definition Web App.

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.0-green.svg)](https://flask.palletsprojects.com/en/2.0.x/)
[![MongoDB](https://img.shields.io/badge/MongoDB-5.0-brightgreen.svg)](https://www.mongodb.com/)
[![PyMongo](https://img.shields.io/badge/PyMongo-3.12-brightgreen.svg)](https://pymongo.readthedocs.io/en/stable/)
[![Docker](https://img.shields.io/badge/Docker-Latest-blue.svg)](https://www.docker.com/)
[![Requests](https://img.shields.io/badge/Requests-2.26-orange.svg)](https://docs.python-requests.org/en/latest/)

####  Описание:
*Функционал*:<br>
	- Поиск шаблона формы по входным данным.<br>		 	

*Входные данные*:<br>
	- Список полей со значениями в теле POST-запроса.<br>

*Выходные данные*:<br>
	- Имя шаблона, либо список полей с указанием типов в случае отсутствия в базе.<br>

*Хранимые данные*<br>
	- В базе данных хранится список шаблонов форм.<br>

*Наполнение базы данных*:
```MongoDB
[
  {
    _id: ObjectId("65623fe6c1ee0aca492650b0"),
    name: 'PersonalInformation',
    first_name: 'Will',
    last_name: 'Bim',
    email_address: 'will.bim@example.com',
    phone_number: ' 7 123 456 78 90'
  },
  {
    _id: ObjectId("65623fe6c1ee0aca492650b1"),
    name: 'ProductOrder',
    product_name: 'Laptop',
    quantity: '2',
    order_date: '2023-11-25'
  },
  {
    _id: ObjectId("65623fe6c1ee0aca492650b2"),
    name: 'Survey',
    question_1: 'What is your favorite color?',
    question_2: 'How often do you exercise?',
    question_3: 'What is your favorite book?'
  },
  {
    _id: ObjectId("65623fe6c1ee0aca492650b3"),
    name: 'EventRegistration',
    event_name: 'Tech Conference',
    participant_name: 'Bob Smith',
    registration_date: '2023-11-25'
  },
  {
    _id: ObjectId("65623fe6c1ee0aca492650b4"),
    name: 'ContactUs',
    sender_name: 'Emily Brown',
    sender_email: 'emily.brown@example.com',
    message: 'Hello, I have a question about your services.'
  }
]
```


## Установка
1. Склонируйте репозиторий:

    ```bash
    git clone git@github.com:bannybaks/forms_filled_definition.git
    cd forms-filled-definition-app
    ```

2. Установите зависимости:

    ```bash
    pip install -r requirements.txt
    ```

## Запуск приложения без базы

1. Запустите веб-приложение:

    ```bash
    python app.py    # запуск в дебаг-режиме
    ```

   Или используйте команду Flask:

    ```bash
    flask run   # запуск в development-режиме
    ```
2. Запуск наполнения тестовая базы в ручном режиме:
   
   ```bash
   python db/filling_database.py
   ```
 
3. Приложение будет доступно по адресу [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

## Запуск приложения в полном окружении

1. Запустите приложение в контейнере Docker:
  > **Note**: база наполняется скриптом при старте контейнеров

  ```bash
  docker-compose up -d
  ```

## Тестирование

1. Запустите тестовый скрипт:

    ```bash
    python test_requests.py
    ```

   Убедитесь, что контейнеры запущены перед выполнением тестов.

## Использование

1. Отправьте POST-запрос как описано ниже с данными формы по адресу [http://127.0.0.1:5000/get_form](http://127.0.0.1:5000/get_form)

## Примеры запросов с возвращаемыми данными:

*Структура ответа*:
- Шаблон найден
```python
# Запрос curl -X POST -d "first_name=Will&phone_number=+7 123 456 78 90&last_name=Bim&email_address=will.bim@example.com" http://127.0.0.1:5000/get_form
{'name': 'ProductOrder'}
```
- Шаблон не найден (поля не найдены, количество переданных полей не имеет значения)
```python
# Запрос curl -X POST -d "work_position=backend&birthday=10.10.2010&grade=junior&work_email=dev@mail.com&contact=+7 999 999 22 22" http://127.0.0.1:5000/get_forms
{
  "work_position": "text",
  "birthday": "date",
  "work_email": "email",
  "phone_num": "phone"
}
```
- Шаблон не найден (поля найдены, количество полей в запросе меньше чем в подходящем шаблоне)
```python
# Запрос curl -X POST -d "first_name=Will&&last_name=Bim&email_address=will.bim@example.com" http://127.0.0.1:5000/get_form
{
  "email_address": "email",
  "first_name": "text",
  "last_name": "text"
}
```