# Prerequisite
- **Postgresql**:
    - Install:
        - For mac OS: Install from official website.
        - For Ubuntu: Ubuntu includes PostgreSQL by default. To install PostgreSQL on Ubuntu:
    ```bash
    apt install postgresql
    ```

- **Django**:
    - Set up a virtual environment (optional but recommended)
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
    - Install Django
    ```bash
    pip install Django
    ```
    - Verify Install
    ```bash
    django-admin --version
    ```
    - Install required Package
    ```bash
    cd server
    pip install -r requirements.txt
    ```
    **Note**: If it shows ```Error: pg_config executable not found.```, it means you have not install the Postgresql.

- **Vue**:
    ```bash
    cd frontend
    npm install
    ```


# Run
It requires three different command line windows.

## run the chat server
docker run -p 6379:6379 -d redis:5

## run the app server
python manage.py runserver

## run the app client
npm run serve
