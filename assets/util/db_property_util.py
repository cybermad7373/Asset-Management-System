import configparser
import os

class DBPropertyUtil:
    @staticmethod
    def get_connection_string(property_file_name):
        try:
            config = configparser.ConfigParser()
            config.read(property_file_name)

            if not config.has_section('Database'):
                raise ValueError("Database section not found in the property file")

            host = config.get('Database', 'host')
            database = config.get('Database', 'database')
            user = config.get('Database', 'user')
            password = config.get('Database', 'password')

            return f"mysql+mysqlconnector://{user}:{password}@{host}/{database}"
        except Exception as e:
            print(f"Error reading property file: {e}")
            raise