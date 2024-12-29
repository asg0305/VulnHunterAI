from neo4j import GraphDatabase

class Neo4jQueries:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def create_person_node(self, name, age):
        query = "CREATE (n:Person {name: $name, age: $age})"
        query = "CREATE (le:Person {name: 'Iratxe' }),  (db:Person {name: 'Asier' }),  (le)-[:KNOWS {since:1768}]->(db)"
        with self.driver.session() as session:
            session.run(query, name=name, age=age)

# Conectarse a Neo4j
neo4j_queries = Neo4jQueries(uri="neo4j://127.0.0.1:7687", user="neo4j", password="password")

# Crear un nodo de tipo Person
neo4j_queries.create_person_node(name="Alice", age=30)

neo4j_queries.close()
