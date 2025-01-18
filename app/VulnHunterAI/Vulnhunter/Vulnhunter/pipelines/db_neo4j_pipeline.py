from neo4j import GraphDatabase
import logging

class Neo4jSecurePipeline:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        print(uri)
        self.node_attributes = {
            "URL": ["url", "source", "num_cve", "num_exploits"],
            "CVE": ["url", "CVE", "CVSSv3", "description", "num_exploits"],
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

        # Verificar si hay enlaces de exploits válidos antes de crear nodos
        if 'Exploit Links' in item and any(link.strip() for link in item['Exploit Links']):
            for exploit_url in item['Exploit Links']:
                if exploit_url.strip():  # Verificar que el enlace no esté vacío
                    logging.debug(f"Creating Exploit node: {exploit_url}")
                    create_exploit_query = """
                    MERGE (exploit:Exploit {url: $exploit_url})
                    SET exploit.url = $exploit_url
                    """
                    session.run(create_exploit_query, exploit_url=exploit_url)

        # Crear nodos para CVEs relacionados y enlazarlos con los exploits
        for cve_data in item.get('CVE_data', []):
            logging.debug(f"Creating CVE node: {cve_data.get('CVE')}")
            create_cve_query = """
            MERGE (cve:CVE {url: $cve_url, CVE: $cve})
            SET cve.url = $cve_url,
                cve.CVSSv3 = $cvssv3,
                cve.description = $description,
                cve.num_exploits = 0
            """
            session.run(create_cve_query, 
                        cve=cve_data.get('CVE'),
                        cve_url=cve_data.get('url', item.get('URL')),
                        cvssv3=cve_data.get('CVSSv3', None),
                        description=cve_data.get('description', None))

            if 'Exploit Links' in item and any(link.strip() for link in item['Exploit Links']):
                for exploit_url in item['Exploit Links']:
                    if exploit_url.strip():  # Verificar que el enlace no esté vacío
                        link_exploit_cve_query = """
                        MATCH (cve:CVE {url: $cve_url, CVE: $cve})
                        MATCH (exploit:Exploit {url: $exploit_url})
                        MERGE (exploit)-[:LINKED_TO]->(cve)
                        SET cve.num_exploits = cve.num_exploits + 1
                        """
                        session.run(link_exploit_cve_query, 
                                    exploit_url=exploit_url,
                                    cve=cve_data.get('CVE'),
                                    cve_url=cve_data.get('url', item.get('URL')))

        # Crear nodo para la URL original y enlazarlo con el CVE
        create_url_query = """
        MERGE (url:URL {url: $url})
        SET url.url = $url,
            url.source = $source,
            url.num_cve = 0,
            url.num_exploits = 0
        """
        session.run(create_url_query, 
                    url=item.get('URL'),
                    source=item.get('source', item.get('URL')))

        for cve_data in item.get('CVE_data', []):
            link_url_cve_query = """
            MATCH (url:URL {url: $url})
            MATCH (cve:CVE {url: $cve_url, CVE: $cve})
            MERGE (cve)-[:LINKED_TO]->(url)
            SET url.num_cve = url.num_cve + 1,
                url.num_exploits = url.num_exploits + cve.num_exploits
            """
            session.run(link_url_cve_query, 
                        url=item.get('URL'),
                        cve=cve_data.get('CVE'),
                        cve_url=cve_data.get('url', item.get('URL')))

        # Añadir un link entre la URL y la Version
        link_url_version_query = """
        MATCH (url:URL {url: $url})
        MATCH (version:Version {version: $version})
        MERGE (url)-[:LINKED_TO]->(version)
        """
        session.run(link_url_version_query, 
                    url=item.get('URL'),
                    version=item.get('version'))

class Neo4jGeneralPipeline:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.node_attributes = {
            "URL": ["url", "source", "num_cve", "num_exploits"],
            "CVE": ["url", "CVE", "num_exploits"],
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

        # Verificar si hay enlaces de exploits válidos antes de crear nodos
        if 'Exploit Links' in item and any(link.strip() for link in item['Exploit Links']):
            for exploit_url in item['Exploit Links']:
                if exploit_url.strip():  # Verificar que el enlace no esté vacío
                    logging.debug(f"Creating Exploit node: {exploit_url}")
                    create_exploit_query = """
                    MERGE (exploit:Exploit {url: $exploit_url})
                    SET exploit.url = $exploit_url
                    """
                    session.run(create_exploit_query, exploit_url=exploit_url)

        # Crear nodos para CVEs relacionados y enlazarlos con los exploits
        for cve_data in item.get('CVE_data', []):
            logging.debug(f"Creating CVE node: {cve_data.get('CVE')}")
            create_cve_query = """
            MERGE (cve:CVE {url: $cve_url, CVE: $cve})
            SET cve.url = $cve_url,
                cve.num_exploits = 0
            """
            session.run(create_cve_query, 
                        cve=cve_data.get('CVE'),
                        cve_url=cve_data.get('url', item.get('URL')))

            if 'Exploit Links' in item and any(link.strip() for link in item['Exploit Links']):
                for exploit_url in item['Exploit Links']:
                    if exploit_url.strip():  # Verificar que el enlace no esté vacío
                        link_exploit_cve_query = """
                        MATCH (cve:CVE {url: $cve_url, CVE: $cve})
                        MATCH (exploit:Exploit {url: $exploit_url})
                        MERGE (exploit)-[:LINKED_TO]->(cve)
                        SET cve.num_exploits = cve.num_exploits + 1
                        """
                        session.run(link_exploit_cve_query, 
                                    exploit_url=exploit_url,
                                    cve=cve_data.get('CVE'),
                                    cve_url=cve_data.get('url', item.get('URL')))

        # Crear nodo para la URL original y enlazarlo con el CVE
        create_url_query = """
        MERGE (url:URL {url: $url})
        SET url.url = $url,
            url.source = $source,
            url.num_cve = 0,
            url.num_exploits = 0
        """
        session.run(create_url_query, 
                    url=item.get('URL'),
                    source=item.get('source', item.get('URL')))

        for cve_data in item.get('CVE_data', []):
            link_url_cve_query = """
            MATCH (url:URL {url: $url})
            MATCH (cve:CVE {url: $cve_url, CVE: $cve})
            MERGE (cve)-[:LINKED_TO]->(url)
            SET url.num_cve = url.num_cve + 1,
                url.num_exploits = url.num_exploits + cve.num_exploits
            """
            session.run(link_url_cve_query, 
                        url=item.get('URL'),
                        cve=cve_data.get('CVE'),
                        cve_url=cve_data.get('url', item.get('URL')))

        # Añadir un link entre la URL y la versión
        link_url_version_query = """
        MATCH (url:URL {url: $url})
        MATCH (version:Version {version: $version})
        MERGE (url)-[:RELATED_TO]->(version)
        """
        session.run(link_url_version_query, 
                    url=item.get('URL'),
                    version=item.get('version'))
