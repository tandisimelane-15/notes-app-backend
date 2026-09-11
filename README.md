# Notes App Backend

## Description

Notes App Backend is a RESTful API built with Flask that allows users to securely create and manage personal notes. Users can create an account, log in and log out using session-based authentication, create notes, view their own notes, update notes and delete notes. Each note is associated with a specific user, ensuring that users can only access and manage their own records.

The application uses SQLAlchemy for database management, Flask-Migrate for database migrations and Flask-Bcrypt for secure password hashing.

## Features

- User registration with secure password hashing
- User login and logout using session-based authentication
- Check active user session
- Create personal notes
- View notes belonging to the logged-in user
- View a specific note
- Update existing notes
- Delete notes
- User-specific authorization to prevent access to another user's notes
- Pagination for retrieving notes efficiently
- Database migrations using Flask-Migrate
- Seed data for testing and development
- Appropriate HTTP status codes and error responses

## How to Run the Project

1. Clone the repository
2. Navigate into the project folder
3. Install the project dependencies with `pipenv install`
4. Enter the virtual environment with `pipenv shell`
5. Set the Flask application with `export FLASK_APP=app.py`
6. Run `flask db upgrade` to apply the database migrations
7. Run the seed file with `python seed.py`
8. Start the Flask server with `flask run --port 5555`
9. The API will be available at `http://localhost:5555`

## Technologies Used

- Python
- Flask
- Flask-SQLAlchemy
- SQLAlchemy
- Flask-Migrate
- Flask-Bcrypt
- Flask-RESTful
- SQLite
- Marshmallow
- Faker
- Pipenv

## API Endpoints

### Authentication

- `POST /signup` — Register a new user
- `POST /login` — Log in an existing user
- `GET /check_session` — Check the currently logged-in user
- `DELETE /logout` — Log out the current user

### Notes

- `GET /notes?page=1&per_page=10` — View the logged-in user's notes with pagination
- `POST /notes` — Create a new note
- `GET /notes/<id>` — View a specific note
- `PATCH /notes/<id>` — Update an existing note
- `DELETE /notes/<id>` — Delete a note

## Future Implementations

- Add note search functionality
- Add categories and tags for organizing notes
- Add note sharing between users
- Add timestamps for created and updated notes
- Add password reset functionality
- Deploy the API to a production environment

## Collaborators

- [Abigail Tandiwe](https://github.com/tandisimelane-15) — Project Structure and Models
- [Teddy Learamo](https://github.com/teddylearamo) — Authentication
- [Gabriel Cosmas](https://github.com/Gabrielcosmas) — Notes CRUD and Authorization
- [Mark Njoroge](https://github.com/Mark-njoroge1) — Pagination, Seeding, Testing and Documentation

## How to Contribute

Pull requests are welcome. For major changes, please open an issue first to discuss the proposed changes.

## License

MIT License

Copyright (c) 2026 Abigail Tandiwe

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## Contact

GitHub: [Abigail Tandiwe](https://github.com/tandisimelane-15)