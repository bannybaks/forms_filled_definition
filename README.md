##  Тестовое задание от LeadHit на позицию Junior Python Developer

###  Web-приложение для определения заполненных форм.
####  Описание:
*Функционал*:
	- Поиск шаблона формы по входным данным.<br>		 	

*Входные данные*:
	- Список полей со значениями в теле POST-запроса.<br>

*Выходные данные*:
	- Имя шаблона, либо список полей с указанием типов в случае отсутствия в базе.<br>

*Хранимые данные*
	- В базе данных хранится список шаблонов форм.<br>

*Структура базы данных*:
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