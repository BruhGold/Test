import os
from dotenv import load_dotenv

load_dotenv()

def connect_to_moodle_database():
    db_type = os.getenv("MOODLE_DB_TYPE")

    if db_type == "mysql":
        import pymysql
        return pymysql.connect(
            host=os.getenv("MOODLE_DB_HOST"),
            user=os.getenv("MOODLE_DB_USER"),
            password=os.getenv("MOODLE_DB_PASSWORD"),
            database=os.getenv("MOODLE_DB_NAME")
        )

    elif db_type == "mssql":
        import pyodbc
        driver = os.getenv("MOODLE_DB_DRIVER")
        server = os.getenv("MOODLE_DB_SERVER")
        return pyodbc.connect(
            f"DRIVER={{{driver}}};"
            f"SERVER={server};"
            f"DATABASE={os.getenv('MOODLE_DB_NAME')};"
            f"UID={os.getenv('MOODLE_DB_USER')};"
            f"PWD={os.getenv('MOODLE_DB_PASSWORD')}"
        )

    elif db_type == "postgres":
        import psycopg2
        return psycopg2.connect(
            host=os.getenv("MOODLE_DB_HOST"),
            user=os.getenv("MOODLE_DB_USER"),
            password=os.getenv("MOODLE_DB_PASSWORD"),
            dbname=os.getenv("MOODLE_DB_NAME")
        )

    else:
        raise ValueError(f"Unsupported DB_TYPE: {db_type}")

# class for color in terminal
# i copied this from stackoverflow
# https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ERROR = '\033[31m'