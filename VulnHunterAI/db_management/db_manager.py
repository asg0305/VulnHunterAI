from neo4j import GraphDatabase
import config

class Neo4jManager:
    def __init__(self):
        self.uri = config.DB_URI
        self.username = config.DB_USERNAME
        self.password = config.DB_PASSWORD
        self.driver = GraphDatabase.driver(self.uri, auth=(self.username, self.password))

    def close(self):
        self.driver.close()

    def get_default_output(self):
        query = """
        MATCH (u:URL)-[r:BELONGS_TO]->(g:Group)
        RETURN u.url AS url, g.name AS group_name
        """
        with self.driver.session() as session:
            result = session.run(query)
            return [{"url": record["url"], "group_name": record["group_name"]} for record in result]

    def get_filtered_columns(self, columns):
        query = f"""
        MATCH (n)
        RETURN {', '.join(columns)}
        """
        with self.driver.session() as session:
            result = session.run(query)
            return [dict(record) for record in result]

    def get_filtered_data(self, query_params):
        filters = " AND ".join([f"n.{key} = ${key}" for key in query_params.keys()])
        query = f"""
        MATCH (n)
        WHERE {filters}
        RETURN n
        """
        with self.driver.session() as session:
            result = session.run(query, **query_params)
            return [dict(record["n"]) for record in result]
