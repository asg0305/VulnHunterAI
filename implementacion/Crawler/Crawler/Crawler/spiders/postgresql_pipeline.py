import psycopg2
from scrapy.exceptions import DropItem

class PostgreSQLPipeline:
    def open_spider(self, spider):
        self.conn = psycopg2.connect(
            host='localhost',
            user='postgres',
            password='yourpassword',
            dbname='scrapy_db'
        )
        self.cursor = self.conn.cursor()

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id SERIAL PRIMARY KEY,
                name TEXT,
                price TEXT,
                availability TEXT
            )
        ''')

    def close_spider(self, spider):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def process_item(self, item, spider):
        try:
            self.cursor.execute("""
                INSERT INTO products (name, price, availability)
                VALUES (%s, %s, %s)
            """, (item.get('name'), item.get('price'), item.get('availability')))
            self.conn.commit()
        except psycopg2.Error as e:
            spider.logger.error(f"Database error: {e}")
            raise DropItem(f"Failed to insert item: {item}")
        return item
