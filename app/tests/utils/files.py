import json 
import csv 
from typing import List, Union

class FileWriter:

    @staticmethod 
    def write_csv_to_path(file_path, data: List[List[str]]):
        with open(file_path, 'w', newline='') as f:
            writer = csv.writer(f, delimiter=',')
            for row in data: 
                writer.writerow(row)

    @staticmethod 
    def write_json_to_path(file_path, data: Union[dict, list]):
        return FileWriter.write_to_path(file_path, json.dumps(data, indent=4))

    @staticmethod 
    def write_to_path(file_path, data):
        with open(file_path, 'w') as f:
            f.write(data)