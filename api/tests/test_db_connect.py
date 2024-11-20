import pymysql
from dotenv import load_dotenv
import os
load_dotenv()

if __name__ == "__main__":
    try:
        connection = pymysql.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_DATABASE"),
            port=int(os.getenv("DB_PORT", 3306))
        )
        print("Connection successful!")
        connection.close()
    except pymysql.MySQLError as e:
        print(f"Connection failed: {e}")
    except Exception as ex:
        print(f"An unexpected error occurred: {ex}")
