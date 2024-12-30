from neo4j import GraphDatabase
import Vulnhunter.Vulnhunter.settings as config

class Neo4jManager:
    def __init__(self):
        self.uri = config.NEO4J_URI
        self.username = config.NEO4J_USER
        self.password = config.NEO4J_PASSWORD
        self.driver = GraphDatabase.driver(self.uri, auth=(self.username, self.password))

    def close(self):
        self.driver.close()

    def get_default_output(self):
        query = """
        MATCH (u:URL)
        RETURN u.url AS url, u.source AS source
        """
        with self.driver.session() as session:
            result = session.run(query)
            return [{"url": record["url"], "source": record["source"]} for record in result]

    def get_filtered_default_output(self, atributo, contenido):
        query = f"""
        MATCH (u:URL)
        WHERE u.{atributo} CONTAINS $contenido
        RETURN u.url AS url, u.source AS source
        """
        with self.driver.session() as session:
            result = session.run(query, contenido=contenido)
            return [{"url": record["url"], "source": record["source"]} for record in result]

    def get_CVEs(self):
        query = """
        MATCH (u:URL)-[:LINKS_TO]->(c:CVE)
        RETURN u.url AS url, u.source AS source, c.CVE AS CVE, c.CVSSv3 AS CVSSv3, c.Description AS description
        """
        with self.driver.session() as session:
            result = session.run(query)
            return [{"url": record["url"], "source": record["source"], "CVE": record["CVE"], "CVSSv3": record["CVSSv3"], "description": record["description"]} for record in result]

    def get_filtered_CVEs(self, atributo, contenido):
        query = f"""
        MATCH (u:URL)-[:LINKS_TO]->(c:CVE)
        WHERE u.{atributo} CONTAINS $contenido OR c.{atributo} CONTAINS $contenido
        RETURN u.url AS url, u.source AS source, c.CVE AS CVE, c.CVSSv3 AS CVSSv3, c.Description AS description
        """
        with self.driver.session() as session:
            result = session.run(query, contenido=contenido)
            return [{"url": record["url"], "source": record["source"], "CVE": record["CVE"], "CVSSv3": record["CVSSv3"], "description": record["description"]} for record in result]

    def get_exploits(self):
        query = """
        MATCH (u:URL)-[:LINKS_TO]->(c:CVE)-[:LINKS_TO]->(e:Exploit)
        RETURN u.url AS url, u.source AS source, c.CVE AS CVE, c.CVSSv3 AS CVSSv3, c.Description AS description, e.url AS exploit_url
        """
        with self.driver.session() as session:
            result = session.run(query)
            return [{"url": record["url"], "source": record["source"], "CVE": record["CVE"], "CVSSv3": record["CVSSv3"], "description": record["description"], "exploit_url": record["exploit_url"]} for record in result]

    def get_filtered_exploits(self, atributo, contenido):
        query = f"""
        MATCH (u:URL)-[:LINKS_TO]->(c:CVE)-[:LINKS_TO]->(e:Exploit)
        WHERE u.{atributo} CONTAINS $contenido OR c.{atributo} CONTAINS $contenido OR e.{atributo} CONTAINS $contenido
        RETURN u.url AS url, u.source AS source, c.CVE AS CVE, c.CVSSv3 AS CVSSv3, c.Description AS description, e.url AS exploit_url
        """
        with self.driver.session() as session:
            result = session.run(query, contenido=contenido)
            return [{"url": record["url"], "source": record["source"], "CVE": record["CVE"], "CVSSv3": record["CVSSv3"], "description": record["description"], "exploit_url": record["exploit_url"]} for record in result]

    def get_related_CVEs(self):
        query = """
        MATCH (u:URL)-[:RELATED_TO]->(c:CVE)
        RETURN u.url AS url, u.source AS source, c.CVE AS CVE, c.CVSSv3 AS CVSSv3, c.Description AS description
        """
        with self.driver.session() as session:
            result = session.run(query)
            return [{"url": record["url"], "source": record["source"], "CVE": record["CVE"], "CVSSv3": record["CVSSv3"], "description": record["description"]} for record in result]

    def get_filtered_related_CVEs(self, atributo, contenido):
        query = f"""
        MATCH (u:URL)-[:RELATED_TO]->(c:CVE)
        WHERE u.{atributo} CONTAINS $contenido OR c.{atributo} CONTAINS $contenido
        RETURN u.url AS url, u.source AS source, c.CVE AS CVE, c.CVSSv3 AS CVSSv3, c.Description AS description
        """
        with self.driver.session() as session:
            result = session.run(query, contenido=contenido)
            return [{"url": record["url"], "source": record["source"], "CVE": record["CVE"], "CVSSv3": record["CVSSv3"], "description": record["description"]} for record in result]

    def get_related_CVEs_exploits(self):
        query = """
        MATCH (u:URL)-[:RELATED_TO]->(c:CVE)-[:LINKS_TO]->(e:Exploit)
        RETURN u.url AS url, u.source AS source, c.CVE AS CVE, c.CVSSv3 AS CVSSv3, c.Description AS description, e.url AS exploit_url
        """
        with self.driver.session() as session:
            result = session.run(query)
            return [{"url": record["url"], "source": record["source"], "CVE": record["CVE"], "CVSSv3": record["CVSSv3"], "description": record["description"], "exploit_url": record["exploit_url"]} for record in result]

    def get_filtered_related_CVEs_exploits(self, atributo, contenido):
        query = f"""
        MATCH (u:URL)-[:RELATED_TO]->(c:CVE)-[:LINKS_TO]->(e:Exploit)
        WHERE u.{atributo} CONTAINS $contenido OR c.{atributo} CONTAINS $contenido OR e.{atributo} CONTAINS $contenido
        RETURN u.url AS url, u.source AS source, c.CVE AS CVE, c.CVSSv3 AS CVSSv3, c.Description AS description, e.url AS exploit_url
        """
        with self.driver.session() as session:
            result = session.run(query, contenido=contenido)
            return [{"url": record["url"], "source": record["source"], "CVE": record["CVE"], "CVSSv3": record["CVSSv3"], "description": record["description"], "exploit_url": record["exploit_url"]} for record in result]
