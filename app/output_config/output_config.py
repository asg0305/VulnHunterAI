import os
import json
from datetime import datetime

class OutputConfig:
    def __init__(self, root_path):
        self.root_path = root_path

    def create_online_search_json_files(self, searchalias, sec_content, gen_content):
        current_time = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        sec_filename = f"{searchalias}-sec-{current_time}.json"
        gen_filename = f"{searchalias}-gen-{current_time}.json"
        filenames = [sec_filename, gen_filename]
        file_paths = []
        for i,filename in enumerate(filenames):
            
            # Crear la estructura del JSON con dos apartados
            if i == 0:
                file_path = os.path.join(self.root_path, "secure-search",filename)
                content = sec_content
                file_paths.append(file_path)
            else:
                file_path = os.path.join(self.root_path, "general-search", filename)
                content = gen_content
                file_paths.append(file_path)
            # Guardar la estructura en el archivo JSON
            with open(file_path, 'w') as json_file:
                json.dump(content, json_file, indent=4)
        return file_paths

    def create_scrapy_jsonl_file(self, searchalias):
        paths = ['cve_finder', 'sec_spider', 'gen_spider']
        current_time = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        filename = f"{searchalias}-{current_time}.jsonl"  # Cambiar la extensión a .jsonl
        complete_paths = []
        for path in paths:
            file_path = os.path.join(self.root_path, path, filename)
            complete_paths.append(file_path)
            # Crear el archivo JSONL pero no escribir nada dentro
            with open(file_path, 'w') as jsonl_file:
                pass  # No escribir nada dentro
        return complete_paths

