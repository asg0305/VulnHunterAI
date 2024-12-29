import json
import os
from itemadapter import ItemAdapter

class JsonWriterPipeline:
    
    def open_spider(self, spider):
        self.file = open('/home/user/output/Vulnhunter/cve_finder/alias-2024-12-25-11-05-16.jsonl', "w")

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(ItemAdapter(item).asdict()) + "\n"
        self.file.write(line)
        return item