import psycopg2
import os
from dotenv import load_dotenv

load_dotenv('../.env')

#Connects to PostgreSQL database and returns if connection is successful
def connect_db():
    try:
        connection = psycopg2.connect(
        dbname = os.getenv('DB_NAME'),
        user = os.getenv('DB_USER'),
        password = os.getenv('DB_PASSWORD'),
        host = os.getenv('DB_HOST'),
        port = os.getenv('DB_PORT')
        )
        print("Connected to PostgreSQL")
        return connection
    except psycopg2.Error as e:
        print(f"Error while connecting to PostgreSQL: {e}")
        return None
def close_db(connection):
    if connection:
        connection.close()
        print("PostgreSQL connection is closed.")








