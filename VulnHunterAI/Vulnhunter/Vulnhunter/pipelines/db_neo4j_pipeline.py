from neo4j import GraphDatabase
import logging

class Neo4jSecurePipeline:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.node_attributes = {
            "URL": ["url", "source"],
            "CVE": ["url", "CVE", "CVSSv3", "Description"],
            "Exploit": ["url"]
        }
        logging.basicConfig(level=logging.DEBUG)

    @classmethod
    def from_crawler(cls, crawler):
        uri = crawler.settings.get('NEO4J_URI')
        user = crawler.settings.get('NEO4J_USER')
        password = crawler.settings.get('NEO4J_PASSWORD')
        return cls(uri, user, password)

    def close_spider(self, spider):
        self.driver.close()

    def process_item(self, item, spider):
        with self.driver.session() as session:
            self._save_url(session, item)
        return item

    def _save_url(self, session, item):
        logging.debug(f"Processing URL: {item.get('URL')}")

        # Crear nodos para los enlaces de exploits
        for exploit_url in item.get('Exploit Links', []):
            logging.debug(f"Creating Exploit node: {exploit_url}")
            create_exploit_query = """
            MERGE (exploit:Exploit {url: $exploit_url})
            SET exploit.url = $exploit_url
            """
            session.run(create_exploit_query, 
                        exploit_url=exploit_url)

        # Crear nodos para CVEs relacionados y enlazarlos con los exploits
        for cve_data in item.get('CVE_data', []):
            logging.debug(f"Creating CVE node: {cve_data.get('CVE')}")
            create_cve_query = """
            MERGE (cve:CVE {url: $cve_url, CVE: $cve})
            SET cve.url = $cve_url,
                cve.CVSSv3 = $cvssv3,
                cve.Description = $description
            """
            session.run(create_cve_query, 
                        cve=cve_data.get('CVE'),
                        cve_url=cve_data.get('url', item.get('URL')),
                        cvssv3=cve_data.get('CVSSv3', None),
                        description=cve_data.get('Description', None))

            for exploit_url in item.get('Exploit Links', []):
                link_exploit_cve_query = """
                MATCH (cve:CVE {url: $cve_url, CVE: $cve})
                MATCH (exploit:Exploit {url: $exploit_url})
                MERGE (cve)-[:LINKS_TO]->(exploit)
                """
                session.run(link_exploit_cve_query, 
                            exploit_url=exploit_url,
                            cve=cve_data.get('CVE'),
                            cve_url=cve_data.get('url', item.get('URL')))

        # Crear nodo para la URL original y enlazarlo con el CVE
        create_url_query = """
        MERGE (url:URL {url: $url})
        SET url.url = $url,
            url.source = $source
        """
        session.run(create_url_query, 
                    url=item.get('URL'),
                    source=item.get('source', item.get('URL')))

        for cve_data in item.get('CVE_data', []):
            link_url_cve_query = """
            MATCH (url:URL {url: $url})
            MATCH (cve:CVE {url: $cve_url, CVE: $cve})
            MERGE (url)-[:LINKS_TO]->(cve)
            """
            session.run(link_url_cve_query, 
                        url=item.get('URL'),
                        cve=cve_data.get('CVE'),
                        cve_url=cve_data.get('url', item.get('URL')))

class Neo4jGeneralPipeline:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.node_attributes = {
            "URL": ["url", "source"],
            "CVE": ["url", "CVE"],
            "Exploit": ["url"]
        }
        logging.basicConfig(level=logging.DEBUG)

    @classmethod
    def from_crawler(cls, crawler):
        uri = crawler.settings.get('NEO4J_URI')
        user = crawler.settings.get('NEO4J_USER')
        password = crawler.settings.get('NEO4J_PASSWORD')
        return cls(uri, user, password)

    def close_spider(self, spider):
        self.driver.close()

    def process_item(self, item, spider):
        with self.driver.session() as session:
            self._save_url(session, item)
        return item

    def _save_url(self, session, item):
        logging.debug(f"Processing URL: {item.get('URL')}")

        # Crear nodos para los enlaces de exploits
        for exploit_url in item.get('Exploit Links', []):
            logging.debug(f"Creating Exploit node: {exploit_url}")
            create_exploit_query = """
            MERGE (exploit:Exploit {url: $exploit_url})
            SET exploit.url = $exploit_url
            """
            session.run(create_exploit_query, 
                        exploit_url=exploit_url)

        # Crear nodos para CVEs relacionados y enlazarlos con los exploits
        for cve_data in item.get('CVE_data', []):
            logging.debug(f"Creating CVE node: {cve_data.get('CVE')}")
            create_cve_query = """
            MERGE (cve:CVE {url: $cve_url, CVE: $cve})
            SET cve.url = $cve_url
            """
            session.run(create_cve_query, 
                        cve=cve_data.get('CVE'),
                        cve_url=cve_data.get('url', item.get('URL')))

            for exploit_url in item.get('Exploit Links', []):
                link_exploit_cve_query = """
                MATCH (cve:CVE {url: $cve_url, CVE: $cve})
                MATCH (exploit:Exploit {url: $exploit_url})
                MERGE (cve)-[:LINKS_TO]->(exploit)
                """
                session.run(link_exploit_cve_query, 
                            exploit_url=exploit_url,
                            cve=cve_data.get('CVE'),
                            cve_url=cve_data.get('url', item.get('URL')))

        # Crear nodo para la URL original y enlazarlo con el CVE
        create_url_query = """
        MERGE (url:URL {url: $url})
        SET url.url = $url,
            url.source = $source
        """
        session.run(create_url_query, 
                    url=item.get('URL'),
                    source=item.get('source', item.get('URL')))

        for cve_data in item.get('CVE_data', []):
            link_url_cve_query = """
            MATCH (url:URL {url: $url})
            MATCH (cve:CVE {url: $cve_url, CVE: $cve})
            MERGE (url)-[:RELATED_TO]->(cve)
            """
            session.run(link_url_cve_query, 
                        url=item.get('URL'),
                        cve=cve_data.get('CVE'),
                        cve_url=cve_data.get('url', item.get('URL')))
