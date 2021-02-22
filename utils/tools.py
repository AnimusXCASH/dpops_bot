import json
import os
from re import search
import sys

project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_path)


class Helpers:
    def __init__(self):
        """
        initiate a object Helper
        """
        pass

    @staticmethod
    def read_json_file(file_name: str):
        """
        Loads the last block height which was stored in last_block.json
        :return: Block height as INT
        """

        # Reads last marked block data in the document
        path = f'{project_path}/{file_name}'
        try:
            with open(path) as json_file:
                data = json.load(json_file)
                return data
        except IOError:
            return None

    def update_json_file(self, file_name: str, key, value):
        """
        Updates Json file based on file name key and value
        """
        try:
            # read data
            data = self.read_json_file(file_name)
            data[key] = value
            path = f'{project_path}/{file_name}'
            with open(path, 'w') as f:
                json.dump(data, f)
            return True
        except FileExistsError as e:
            print(e)
            return False
