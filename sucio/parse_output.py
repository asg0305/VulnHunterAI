import os
import glob
import json
from datetime import datetime
import output_config.config as config
from output_config.parse_content import ParseContent

class ParseOutput:
    def __init__(self, group_name):
        self.sec_domains = getattr(config, "sec_domains")
        self.gen_domains = getattr(config, "general_domains")
        self.data = group_name
        self.paths = getattr(config, self.data)
        self.parser = ParseContent(self.sec_domains, self.gen_domains)
        if self.paths is None:
            raise ValueError(f"No paths found for group: {group_name} in {self.data}")

    def parse(self, searchalias):
        results = []
        for path, attributes in self.paths.items():
            # Sustituir parámetros en el formato del archivo
            file_pattern = attributes['format'].format(searchalias=searchalias, date='*')
            file_process_mode = attributes['process_mode']
            print("FILE PATTERN")
            print(file_pattern)
            matching_files = self._find_matching_files(path, file_pattern)
            print("Matching files")
            print(matching_files)
            # Encontrar el archivo más reciente
            most_recent_file = self._get_most_recent_file(file_pattern, matching_files)
            print("MOST RECENT")
            print(most_recent_file)
            if most_recent_file and os.path.exists(most_recent_file):
                file_type = self._extract_file_type(most_recent_file)
                file_results = self.read_file_type(most_recent_file, file_type)
                print('FILE RESULTS')
                print(file_results)
                content = self.parser.parse_content(file_results, file_process_mode)
                results.extend(content)
        print(results)
        return results

    def _find_matching_files(self, directory, pattern):
        files = glob.glob(os.path.join(directory, pattern))
        return files

    def _extract_file_type(self, file_path):
        # Extraer el tipo de archivo del nombre del archivo
        if file_path.endswith('.jsonl'):
            return 'jsonl'
        return 'json'

    def read_file_type(self, file_path, file_type):
        # Leer el archivo según su tipo
        if file_type == 'jsonl':
            return self._read_jsonl(file_path)
        return self._read_json(file_path)

    def _read_json(self, file_path):
        with open(file_path, 'r') as file:
            return json.load(file)

    def _read_jsonl(self, file_path):
        results = []
        with open(file_path, 'r') as file:
            for line in file:
                results.append(json.loads(line))
        return results

    def _get_most_recent_file(self, format, files):
        most_recent_file = None
        most_recent_date = None
        date_format = '%Y-%m-%d-%H-%M-%S'
        for file in files:
            # Extraer la fecha del nombre del archivo
            filename = os.path.basename(file)
            print(filename)
            date_str = ('').join(('-').join(filename.split('-')[2:]).split('.')[0])
            print(date_str)
            file_date = datetime.strptime(date_str, date_format)
            if not most_recent_date or file_date > most_recent_date:
                most_recent_date = file_date
                most_recent_file = file
        return most_recent_file
