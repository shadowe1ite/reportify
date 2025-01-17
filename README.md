# Reportify

Welcome to Reportify, your AI-powered solution for generating comprehensive event reports.

### pre-requirements

1. create a .env file inside the cloned repo
2. add
    ```bash
    ENVIRONMENT=development
    SECRET_KEY="<Django_Secret_Key>"
    DATABASE_URL="<Your_Database_Url>" # only if you have one or run locally using sqlite3
    ```

### setup

1. initialize python virtual environment
    ```bash
    python3 -m venv .venv  
    source .venv/bin/activate
    ```
2. install requirements
    ```bash
    pip install -r requirements.txt 
    ```


### Running app

```bash
python manage.py runserver 
```

then visit http://127.0.0.1:8000/