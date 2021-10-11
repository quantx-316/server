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


class FileReader:

    @staticmethod
    def read_json_from_path(file_path):
        info = FileReader.read_from_path(file_path)
        return json.loads(info)

    @staticmethod
    def read_from_path(file_path):
        with open(file_path) as f:
            info = f.read()
            return info
