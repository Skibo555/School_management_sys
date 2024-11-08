# School Management System

The project: School_Management_System is a RESTfuL API built with python FastAPI. It exposes endpoints to create a user, login an existing user and also gives the users to change their password, this changing of password can only be done if the user still has access to the email used to register, if not the account can't be retrieved again, even from the backend can't help recover it.


## Features
- User Authentication: register, login, password management, create_user (which can only be done by an admin, not even a lecturer).
- User Management: CRUD operations for users with different roles (e.g., student, lecturer, admins, supper, course rep).
- Course Management: CRUD operations for creating courses.
- It uses strict RBAC (Role Based Access Control) approach.

[//]: # (- Event Management: CRUD operations for managing events.)
[//]: # (- Position Management: Assign users to roles or positions within a course or class.)

## Technologies Used

- Python
- FastAPI
- MongoDB (using odmantic for schema and data modeling)
- JWT for Authentication and Authorization
- Pydantic for Data Validation
- bcrypt for Password Hashing

## Prerequisites

- **Python** (version >= 3.3)
- **pip** (Python package manager)
- **MongoDB** (local or cloud instance)

## Setup

1. Clone the repository:
```bash 
git clone  https://github.com/Skibo555/School_management_sys.git 
```
2. cd into the project directory:
```bash 
cd School_management_sys/api
```
3.  Install the dependencies:
```bash 
pip install -r requirements.txt
```
6. Run the app:
```bash 
python3 main.py
```

- You can [click here](https://school-management-sys-6u4e.onrender.com) to visit the live version of this project 🍗

## License
This project is licensed under the MIT License.
