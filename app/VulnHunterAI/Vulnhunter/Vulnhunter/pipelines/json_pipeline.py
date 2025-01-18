import json

from itemadapter import ItemAdapter


class CVEFinderPipeline:
    def open_spider(self, spider):
        self.file = open("/home/user/output/Vulnhunter/cve_finder/cve_finder.jsonl", "w")

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(ItemAdapter(item).asdict()) + "\n"
        self.file.write(line)
        return item
    
class SecPipeline:
    def open_spider(self, spider):
        self.file = open("/home/user/output/Vulnhunter/sec_spider/sec_spider.jsonl", "w")

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(ItemAdapter(item).asdict()) + "\n"
        self.file.write(line)
        return item
    
class GenPipeline:
    def open_spider(self, spider):
        self.file = open("/home/user/output/Vulnhunter/gen_spider/gen_spider.jsonl", "w")

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(ItemAdapter(item).asdict()) + "\n"
        self.file.write(line)
        return item