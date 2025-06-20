import mysql.connector
from mysql.connector import Error
from .db_property_util import DBPropertyUtil

class DBConnUtil:
    @staticmethod
    def get_connection(connection_string=None, property_file_name=None):
        try:
            if property_file_name:
                connection_string = DBPropertyUtil.get_connection_string(property_file_name)

            if not connection_string:
                raise ValueError("No connection string provided")

            # Parse the connection string
            parts = connection_string.split('://')[1].split('@')
            user_pass = parts[0].split(':')
            host_db = parts[1].split('/')

            user = user_pass[0]
            password = user_pass[1]
            host = host_db[0]
            database = host_db[1]

            connection = mysql.connector.connect(
                host=host,
                database=database,
                user=user,
                password=password
            )

            if connection.is_connected():
                print("Connected to MySQL database")
                return connection

        except Error as e:
            print(f"Error while connecting to MySQL: {e}")
            raise