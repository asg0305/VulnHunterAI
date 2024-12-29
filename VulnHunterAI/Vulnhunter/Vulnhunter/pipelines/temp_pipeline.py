class TempPipeline:
    def __init__(self):
        self.items = []

    def process_item(self, item, spider):
        self.items.append(item)
        print("Desde pipeline 2")
        print(self.items[1])
        return item

    def get_items(self):
        print("Desde pipeline")
        print(self.items)
        return self.items

    def clear_items(self):
        self.items = []
