import psycopg2
import os

from dotenv import load_dotenv

class db_setup:
    # load environment variables
    load_dotenv()


    # Assign env variables for pgSQL connection
    db_host = os.environ["db_host"]
    db_port = os.environ["db_port"]
    db_database = os.environ["db_database"]
    db_user = os.environ["db_user"]
    db_password = os.environ["db_password"]
    db_schema = os.environ["db_schema"]

    #Connect to pgSQL
    def create_database(self):
        connection = psycopg2.connect(host=self.db_host,port=self.db_port,user=self.db_user,password=self.db_password,database="postgres")
        CREATE_DATABASE = f"CREATE DATABASE {self.db_database}"
        GRANT = f"GRANT ALL PRIVILEGES ON DATABASE {self.db_database} to {self.db_user}"
        connection.autocommit = True 
        try:
            cursor = connection.cursor()
            cursor.execute(CREATE_DATABASE)
            cursor.execute(GRANT)
            cursor.close()
            connection.close()
            return {"process":"create_database","status":"success"}
        except(psycopg2.DatabaseError, Exception) as error:
            print(error)
            connection.close()
            return {"process":"create_database","status":"failed","message":error}
        

    #Build SCHEMA
    def create_schema_table(self):
        connection = psycopg2.connect(host=self.db_host,port=self.db_port,database=self.db_database,user=self.db_user,password=self.db_password)
        CREATE_SCHEMA = f"CREATE SCHEMA IF NOT EXISTS {self.db_schema};"
        CREATE_TABLE_STRING = f"""CREATE TABLE IF NOT EXISTS {self.db_schema}.string (
                            id SERIAL PRIMARY KEY,
                            sku VARCHAR(255) NOT NULL,
                            similar_sku VARCHAR(255) NOT NULL,
                            score FLOAT NOT NULL,
                            rank INTEGER,
                            count_appearances_as_similar_sku INTEGER);"""
        CREATE_TABLE_NUM = f"""CREATE TABLE IF NOT EXISTS {self.db_schema}.numerical (
                            id SERIAL PRIMARY KEY,
                            sku VARCHAR(255) NOT NULL,
                            similar_sku VARCHAR(255) NOT NULL,
                            score FLOAT NOT NULL,
                            rank INTEGER,
                            count_appearances_as_similar_sku INTEGER);"""

        # Create Schema and Tables:
        try:
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute(CREATE_SCHEMA)
                    cursor.execute(CREATE_TABLE_STRING)
                    cursor.execute(CREATE_TABLE_NUM)
                    return {"process":"create_schema","status":"success"}
        except(psycopg2.DatabaseError, Exception) as error:
            print(error)
            return {"process":"create_schema","status":"failed","message":error}

    if __name__ == '__main__':
        create_database()
        create_schema_table()