import psycopg
from db import get_connection
from controller import Controller


if __name__ == "__main__":
    try:
        with get_connection():
            pass
        Controller().run()
    except psycopg.OperationalError:
        print("error: cannot connect to PostgreSQL, check the .env file")