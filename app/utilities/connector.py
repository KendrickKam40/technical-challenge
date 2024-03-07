import os
import psycopg2
from sqlalchemy import create_engine
from dotenv import load_dotenv
import pandas as pd
from subprocess import PIPE,Popen
from .process_data import processor
from classes import FileItem


class Connector:
    db_host:str
    db_port: str
    db_database: str
    db_user: str
    db_password: str
    database_schema: str
    json_files: list[FileItem]
    process: processor

    #Setup environment variables, JSON file objects and the processor instance
    def __init__(self, json_files:list[FileItem]):
        load_dotenv()
        # Assign env variables for pgSQL connection
        self.db_host = os.environ["db_host"]
        self.db_port = os.environ["db_port"]
        self.db_database = os.environ["db_database"]
        self.db_user = os.environ["db_user"]
        self.db_password = os.environ["db_password"]

        #assign env variables for uploading data to pgSQL
        self.database_schema = os.environ["db_schema"]

        self.json_files = json_files

        self.process = processor()

    #Read files in the JSON list
    def read_files(self) -> pd.DataFrame:
        try:
            self.process.read_json(self.json_files)
            ret: pd.DataFrame = self.process.get_dataframe()
            return ret
        except Exception as e:
            msg = {"process":"read_files", "status":"failed","message":"Unable to read JSON files"}
            return None
    
    #Upload dataframe to postgresql database
    def upload_to_pg(self, df: pd.DataFrame) -> object:
        try:
            engine = create_engine(f'postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_database}')
            for file in self.json_files:
                #get table name to insert
                table_name = file.database
                #get appropriate df slice from the larger pandas df
                df_to_insert = df.loc[df['source'] == table_name]
                #rename/remove uneccesary columns
                df_renamed = df_to_insert.rename(columns={'similarity_score':'score'})
                df_renamed = df_renamed.drop('source', axis=1)
                #run SQL query
                df_renamed.to_sql(name=table_name, con=engine, schema=self.database_schema,index=False, if_exists='append')

                return {"process":"upload","status":"success"}
        except:
            return {"process":"upload","status":"failed","message":"Error uploading to database."}

    # FOR TESTING PURPOSES - Function to delete all table data
    def delete_postgres_data(self):
        try:
            connection = psycopg2.connect(host=self.db_host,port=self.db_port,database=self.db_database,user=self.db_user,password=self.db_password)
            cursor = connection.cursor()

            for file in self.json_files:
                table_name = file.database
                delete_tbl_data = f"DELETE FROM {self.database_schema}.{table_name};"
                cursor.execute(delete_tbl_data)
            connection.commit()
            cursor.close()
            connection.close()

            return {"process":"delete_database","status":"success"}
        except:
            print("Error deleting database")
            return {"process":"delete_database","status":"failed","message":"Error deleting database"}

    # Dump Schema - Note: A compatible version of postgresql must be installed for pg_dumps to work
    def dump_schema(self,filename="./solution_dump.sql"):
        try:
            command = f'pg_dump --host={self.db_host} ' \
                    f'--dbname={self.db_database} ' \
                    f'--port={self.db_port} ' \
                    f'--schema={self.database_schema} ' \
                    f'--username={self.db_user} ' \
                    f'--file={filename}'
            proc = Popen(command, shell=True, env={**os.environ,
                    'PGPASSWORD': self.db_password
                })
            proc.wait()
            return {"process":"schema_dump","status":"success"}
        except:
            print("Error dumping schema")
            return {"process":"schema_dump","status":"failed","message":"Error dumping schema"}


