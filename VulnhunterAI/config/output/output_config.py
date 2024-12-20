import os
import json
from datetime import datetime

class OutputConfig:
    def __init__(self, root_path):
        self.root_path = root_path

    def create_json_files(self, searchalias, content):
        current_time = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        filename = f"{searchalias}-{current_time}.json"

        file_path = os.path.join(self.root_path, filename)
        with open(file_path, 'w') as json_file:
            json.dump(content, json_file, indent=4)