from fastapi import FastAPI
from pydantic import BaseModel, Field

from utilities.db_setup import db_setup
from utilities.connector import Connector

app = FastAPI()

#Setup DB schema and database if it doesnt exist
setup = db_setup()
setup.create_database()
setup.create_schema_table()


class FileItem(BaseModel):
    database : str = Field(description="table name to upload the JSON file to")
    filepath : str = Field(description="JSON filename")



class Upload(BaseModel):
    files_to_upload: list[FileItem] = Field(description="list of files to upload along with the table name")
    deleteExistingData: bool = Field(description="Flag to delete existing data in the PGSQL database before uploading files")
    dumpSchema: bool = Field(description="Flag to run the pg_dump command after uploading data")



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



