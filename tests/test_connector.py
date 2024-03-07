from app.utilities.connector import Connector
import pandas as pd


def test_default_env_vars():
    json_files=  [
            {
                "database" : "string",
                "filepath" : "sku_similarities_string_method.json"
            },
            {
                "database" : "numerical",
                "filepath" : "sku_similarities_numerical_method.json"
            }
        ]
    conn = Connector(json_files)

    assert conn.database_schema == 'mytest'
    assert conn.db_host == 'db'
    assert conn.json_files == json_files
    assert conn.db_port == '5432'
    assert conn.db_password == 'admin123'
    assert conn.db_user == 'admin'
    assert conn.db_database == 'mydatabase'

def test_read_files():
    json_files=  [
            {
                "database" : "string",
                "filepath" : "sku_similarities_string_method.json"
            },
            {
                "database" : "numerical",
                "filepath" : "sku_similarities_numerical_method.json"
            }
        ]
    conn = Connector(json_files)

    df = conn.read_files()

    assert df is not None

def test_upload_data():
    json_files=  [
            {
                "database" : "string",
                "filepath" : "sku_similarities_string_method.json"
            },
            {
                "database" : "numerical",
                "filepath" : "sku_similarities_numerical_method.json"
            }
        ]
    conn = Connector(json_files)

    df = conn.read_files()

    status = conn.upload_to_pg(df)

    assert status == {"process":"upload","status":"success"}

def test_delete_data():
    json_files=  [
            {
                "database" : "string",
                "filepath" : "sku_similarities_string_method.json"
            },
            {
                "database" : "numerical",
                "filepath" : "sku_similarities_numerical_method.json"
            }
        ]
    conn = Connector(json_files)

    df = conn.read_files()
    conn.upload_to_pg(df)
    status = conn.delete_postgres_data()


    assert status == {"process":"delete_database","status":"success"}


def test_schema_dump():
    json_files=  [
            {
                "database" : "string",
                "filepath" : "sku_similarities_string_method.json"
            },
            {
                "database" : "numerical",
                "filepath" : "sku_similarities_numerical_method.json"
            }
        ]
    conn = Connector(json_files)

    df = conn.read_files()
    conn.upload_to_pg(df)
    status = conn.dump_schema()


    assert status == {"process":"schema_dump","status":"success"}