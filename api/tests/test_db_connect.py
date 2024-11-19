from sqlalchemy import create_engine
import pymysql

if __name__ == "__main__":
    try:
        connection = pymysql.connect(
            host='127.0.0.1',
            user='root',
            password='root',
            database='sandwich_maker_api',
            port=3306
        )
        print("Connection successful!")
        connection.close()
    except pymysql.MySQLError as e:
        print(f"Connection failed: {e}")
    except Exception as ex:
        print(f"An unexpected error occurred: {ex}")
