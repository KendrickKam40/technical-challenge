from fastapi import FastAPI
from classes import FileItem, Upload
from utilities.db_setup import db_setup
from utilities.connector import Connector

app = FastAPI()

#Setup DB schema and database if it doesnt exist
setup = db_setup()
setup.create_database()
setup.create_schema_table()


@app.post("/api/v1/setup/createDB/")
async def create_database():
    setup = db_setup()
    create_database = setup.create_database()
    create_schema = setup.create_schema_table()

    return [create_database,create_schema]

@app.post("/api/v1/upload/data")
async def upload_data(upload_body: Upload):
    response = []

    files_to_read = upload_body.files_to_upload
    cnx = Connector(json_files=files_to_read)

    return_data = cnx.read_files()

    if(upload_body.deleteExistingData):
        delete_response = cnx.delete_postgres_data()
        response.append(delete_response)
    
    #commence upload
    upload_response = cnx.upload_to_pg(df=return_data)
    response.append(upload_response)
    #dump schema file
    if(upload_body.dumpSchema):
        dump_response = cnx.dump_schema()
        response.append(dump_response)
    response.append({"status":200})
    return response



