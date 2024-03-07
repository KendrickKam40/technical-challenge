from pydantic import BaseModel, Field

class FileItem(BaseModel):
    database : str = Field(description="table name to upload the JSON file to")
    filepath : str = Field(description="JSON filename")


class Upload(BaseModel):
    files_to_upload: list[FileItem] = Field(description="list of files to upload along with the table name")
    deleteExistingData: bool = Field(description="Flag to delete existing data in the PGSQL database before uploading files")
    dumpSchema: bool = Field(description="Flag to run the pg_dump command after uploading data")

