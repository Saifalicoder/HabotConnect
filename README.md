## Employee Management API Setup

### Prerequisites
- **Python 3.x** must be installed.
- **pip** (Python package installer) must be available.

### Steps to Setup the Project Locally
1. **Clone the Repository and setup virtual environment**
   ```bash
   git clone https://github.com/Saifalicoder/HabotConnect.git
   cd yourrepository
   cd yourproject
   python -m venv venv
   venv\Scripts\activate
   ```
2. **Install Required Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Setup Database**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```
3. **IRun the Development Server**
   ```bash
   python manage.py runserver
   ```
## Backend API Doc

## Signup

|![Static Badge](https://img.shields.io/badge/Method-POST-GREEN)| ```/api/signup/``` |
| :-------- | :------------------------- |

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `username` | `string` | **Required.** username |
| `email`| `string`  | **Required.** email |
| `password`| `string`  | **Required.** password |


**Example**
```http
{
    "username": "username",
    "email":"email@email.com",
    "password": "password",
}
```
**Response**
```http
{
    "message": "User created successfully"
}
```

## Login

|![Static Badge](https://img.shields.io/badge/Method-POST-GREEN)| ```/api/token/``` |
| :-------- | :------------------------- |

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `username` | `string` | **Required.** username |
| `password`| `string`  | **Required.** password |


**Example**
```http
{
    "username": "username",
    "password": "password",
}
```
**Response**
```http
{
    "refresh": "refresh_token",
    "access": "access_token"
}
```
## Create an Employee

|![Static Badge](https://img.shields.io/badge/Authenticated%20User-blue)|![Static Badge](https://img.shields.io/badge/Method-POST-GREEN)| ```/api/employees/``` |
| :-------- | :-------- | :------------------------- |

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `name` | `string` | **Required.** Your name |
| `email`| `string`  | **Required.** Your Email |
| `department`| `string`  | **Not Required.** Department name |
| `role`| `string`  |**Not Required.** Role name   |


**Example**
```http
{
    "name": "first_name",
    "email": "testemail@gmail.com",
    "department": "department",
    "role": "role_name"
}
```
## Get an Employee

|![Static Badge](https://img.shields.io/badge/Authenticated%20User-blue)|![Static Badge](https://img.shields.io/badge/Method-GET-blue)| ```/api/employees/{id}``` |
| :-------- | :-------- | :------------------------- |

**Response**
```http
{
    "id":1,
    "name": "first_name",
    "email": "testemail@gmail.com",
    "department": "department",
    "role": "role_name",
    "date_joined":"2024-11-02"
}
```

## Update an Employee

|![Static Badge](https://img.shields.io/badge/Authenticated%20User-blue)|![Static Badge](https://img.shields.io/badge/Method-PUT-yellow)| ```/api/employees/{id}``` |
| :-------- | :-------- | :------------------------- |


**Payload**
```http
{
    "name": "new_name",
}
```
**Response**
```http
{
    "id":1,
    "name": "new_name",
    "email": "testemail@gmail.com",
    "department": "department",
    "role": "role_name",
    "date_joined":"2024-11-02"
}
```

## Delete an Employee

|![Static Badge](https://img.shields.io/badge/Authenticated%20User-blue)|![Static Badge](https://img.shields.io/badge/Method-DELETE-red)| ```/api/employees/{id}``` |
| :-------- | :-------- | :------------------------- |


**Response**
```http
{
    "status": "204 No Content",
}
```
## Run Tests
![image](https://github.com/user-attachments/assets/6b266481-7ad1-42d8-87e2-fe828dfc207c)

