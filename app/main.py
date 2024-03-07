from fastapi import FastAPI
from classes import FileItem, Upload
from utilities.db_setup import db_setup
from utilities.connector import Connector

app = FastAPI()

#Setup DB schema and database if it doesnt exist
setup = db_setup()
setup.create_database()
setup.create_schema_table()

@app.post("/api/v1/upload/data")
async def upload_data(upload_body: Upload):
    response = []
    #Read files from request body
    files_to_read = upload_body.files_to_upload

    #Setup connection instance
    cnx = Connector(json_files=files_to_read)

    #Read JSON files
    return_data = cnx.read_files()

    #Delete existing db entries in postgresql if needed
    if(upload_body.deleteExistingData):
        delete_response = cnx.delete_postgres_data()
        response.append(delete_response)
    
    #commence upload
    upload_response = cnx.upload_to_pg(df=return_data)
    response.append(upload_response)
    response.append({"status":200})
    return response