## Forms Filled Definition Web App

[![Python](https://img.shields.io/badge/Python-3.10-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.0-green.svg)](https://flask.palletsprojects.com/en/2.0.x/)
[![MongoDB](https://img.shields.io/badge/MongoDB-5.0-brightgreen.svg)](https://www.mongodb.com/)
[![PyMongo](https://img.shields.io/badge/PyMongo-3.12-brightgreen.svg)](https://pymongo.readthedocs.io/en/stable/)
[![Docker](https://img.shields.io/badge/Docker-Latest-blue.svg)](https://www.docker.com/)
[![Requests](https://img.shields.io/badge/Requests-2.26-orange.svg)](https://docs.python-requests.org/en/latest/)

####  Description:
*Functional*:<br>
- Search for a form template based on input data.<br>

*Input data*:<br>
- List of fields with values in the body of the POST request.<br>

*Imprint*:<br>
- Template name, or a list of fields indicating types if not in the database.<br>

*Stored data*<br>
- The database stores a list of form templates.<br>

*Filling the database*:
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


## Installation
1. Clone the repository:

     ```bash
     git clone git@github.com:bannybaks/forms_filled_definition.git
     cd forms-filled-definition-app
     ```

2. Install dependencies:

     ```bash
     pip install -r requirements.txt
     ```

## Running an application without a database

1. Launch the web application:

     ```bash
     python app.py # run in debug mode
     ```

    Or use the Flask command:

     ```bash
     flask run # run in development mode
     ```
2. Start filling the test database manually:
   
    ```bash
    python db/filling_database.py
    ```
 
3. The application will be available at [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

## Running the application in full environment

1. Run the application in a Docker container:
   > **Note**: the database is filled with a script when containers start

   ```bash
   docker-compose up -d
   ```

## Testing

1. Run the test script:

     ```bash
     python test_requests.py
     ```

    Make sure containers are running before running tests.

## Usage

1. Send a POST request as described below with the form data to [http://127.0.0.1:5000/get_form](http://127.0.0.1:5000/get_form)

## Examples of queries with returned data:

*Answer structure*:
- Pattern found
```python
# Request curl -X POST -d "first_name=Will&phone_number=+7 123 456 78 90&last_name=Bim&email_address=will.bim@example.com" http://127.0.0.1:5000/get_form
{'name': 'ProductOrder'}
```
- Template not found (no fields found, number of fields passed does not matter)
```python
# Request curl -X POST -d "work_position=backend&birthday=10.10.2010&grade=junior&work_email=dev@mail.com&contact=+7 999 999 22 22" http://127.0.0.1:5000/get_forms
{
   "work_position": "text",
   "birthday": "date",
   "work_email": "email",
   "phone_num": "phone"
}
```
- Template not found (fields found, the number of fields in the request is less than in a suitable template)
```python
# Request curl -X POST -d "first_name=Will&&last_name=Bim&email_address=will.bim@example.com" http://127.0.0.1:5000/get_form
{
   "email_address": "email",
   "first_name": "text",
   "last_name": "text"
}
```
