# TalentMatch

A recruitment platform connecting candidates and employers. Built with Django and PostgreSQL.

## Requirements

- Python 3.13
- PostgreSQL installed and running
- Git

## Setup

1. Clone the repository and navigate to the project folder:
   ```
   git clone https://github.com/Vatsal1s/CSIT314
   cd CSIT314
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   venv\Scripts\activate
   ```
   If you get an error about Python not being found then run `where.exe python` to find your Python path, then use that path to create the venv:
   ```
   & "C:\path\to\python.exe" -m venv venv
   ```

3. Install dependencies:
   ```
   pip install django psycopg2-binary python-decouple
   ```

4. Create a PostgreSQL database and note your credentials.

5. Create a `.env` file in the project root with your database details:
   ```
   DB_NAME=your_database_name
   DB_USER=your_username
   DB_PASSWORD=your_password
   DB_HOST=localhost
   DB_PORT=5432
   ```

6. Apply migrations:
   ```
   python manage.py migrate
   ```

7. Run the development server:
   ```
   python manage.py runserver
   ```

8. Open `http://127.0.0.1:8000` in your browser. The landing page loads where users can sign up as a candidate or employer.
