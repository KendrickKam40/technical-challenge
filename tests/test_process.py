from app.utilities.process_data import processor
import pandas as pd


def test_default_env_vars():
    proc = processor()
    assert proc.data_file_path == "./data_in"

def test_read_json():
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
    proc = processor()
    proc.read_json(json_files)

    df = proc.get_dataframe()

    assert df is not None