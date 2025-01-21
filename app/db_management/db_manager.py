from neo4j import GraphDatabase
import VulnHunterAI.Vulnhunter.Vulnhunter.settings as config

class Neo4jManager:
    def __init__(self):
        self.uri = config.NEO4J_URI
        self.username = config.NEO4J_USER
        self.password = config.NEO4J_PASSWORD
        self.driver = GraphDatabase.driver(self.uri, auth=(self.username, self.password))
        self.data_parameters = config.DATA_PARAMETERS
        self.project_alias = None
        self.srv_os = None
        self.version = None

    def close(self):
        self.driver.close()
    
    def add_search(self, project_alias, srv_os, version):
        with self.driver.session() as session:
            session.write_transaction(self._merge_data, project_alias, srv_os, version)
        self.update_attributes(self.project_alias)
    
    def set_params(self, alias, srv_os, version):
        self.project_alias = alias
        self.srv_os = srv_os
        self.version = version

    @staticmethod
    def _merge_data(tx, project_alias, srv_os, version):
        query = """
        MERGE (p:Project {alias: $project_alias})
        ON CREATE SET p.source_num = $source_num, p.cve_num = $cve_num, p.exploit_num = $exploit_num
        MERGE (s:SrvOS {srv_os: $srv_os})
        ON CREATE SET s.source_num = $source_num, s.cve_num = $cve_num, s.exploit_num = $exploit_num
        MERGE (v:Version {version: $version})
        ON CREATE SET v.source_num = $source_num, v.cve_num = $cve_num, v.exploit_num = $exploit_num
        MERGE (p)<-[:LINKED_TO]-(s)
        MERGE (s)<-[:LINKED_TO]-(v)
        """
        tx.run(query, project_alias=project_alias, srv_os=srv_os, version=version, source_num=0, cve_num=0, exploit_num=0)
    
    def update_attributes(self, project_alias):
        with self.driver.session() as session:
            session.write_transaction(self._update_attributes, project_alias)

    @staticmethod
    def _update_attributes(tx, project_alias):
        query = """
        MATCH (p:Project {alias: $project_alias})<-[:LINKED_TO]-(s:SrvOS)<-[:LINKED_TO]-(v:Version)
        OPTIONAL MATCH (url:URL)-[:RELATED_TO|LINKED_TO]->(v)
        OPTIONAL MATCH (cve:CVE)-[:RELATED_TO|LINKED_TO]->(url)
        OPTIONAL MATCH (exploit:Exploit)-[:LINKED_TO]->(cve)
        WITH p, s, v, url, cve, count(DISTINCT exploit.url) AS exploit_count
        SET cve.num_exploits = exploit_count
        WITH p, s, v, url, cve, count(cve.CVE) AS cve_count, sum(cve.num_exploits) AS url_exploit_count
        SET url.num_cve = cve_count, url.num_exploits = url_exploit_count
        WITH p, s, v, url, sum(url.num_exploits) AS v_exploit_count, count(DISTINCT cve) AS v_cve_count, count(url) AS v_source_count
        SET v.exploit_num = v_exploit_count, v.cve_num = v_cve_count, v.source_num = v_source_count
        WITH p, s, v, sum(v.source_num) AS srv_source_num, sum(v.cve_num) AS srv_cve_num, sum(DISTINCT v.exploit_num) AS srv_exploit_num
        SET s.source_num = srv_source_num, s.cve_num = srv_cve_num, s.exploit_num = srv_exploit_num
        WITH p, s, v, sum(s.source_num) AS proj_source_num, sum(DISTINCT s.cve_num) AS proj_cve_num, sum(DISTINCT s.exploit_num) AS proj_exploit_num
        SET p.source_num = proj_source_num, p.cve_num = proj_cve_num, p.exploit_num = proj_exploit_num
        RETURN p.source_num AS p_source_num, p.cve_num AS p_cve_num, p.exploit_num AS p_exploit_num
        """
        tx.run(query, project_alias=project_alias)


    def filter_parameters(self, request_data):
        selected_parameters = []
        for data in request_data:
            print(f"Searching {data}")
            data = data.strip()
            for node, properties in self.data_parameters.items():
                for prop in properties:
                    print(f"Comparing {data} == {node}.{prop}")
                    if data == f"{node}.{prop}":
                        selected_parameters.append(f"{node}.{prop}")
        return selected_parameters

    def get_data_by_columns(self, project_alias, srv_os, version, columns):
        columns_query = ", ".join(columns)
        match_clauses = [f"MATCH (Project:Project {{alias: '{project_alias}'}})"]
        if srv_os:
            match_clauses.append(f"MATCH (p)<-[:LINKED_TO]-(SrvOS:SrvOS {{srv_os: '{srv_os}'}})")
        if version:
            match_clauses.append(f"MATCH (s)<-[:LINKED_TO]-(Version:Version {{version: '{version}'}})")
        match_clauses.append("MATCH (Version)<-[:LINKED_TO]-(URL:URL)") 
        match_clauses.append("MATCH (URL)<-[:LINKED_TO]-(CVE:CVE)") 
        match_clauses.append("MATCH (CVE)<-[:LINKED_TO]-(Exploit:Exploit)")
    
        # Construir la cláusula RETURN
        columns_query = ", ".join(columns)
    
        # Unir todas las partes de la consulta
        query = "\n".join(match_clauses)
        query += f"\nRETURN {columns_query}"

        return query

    def get_results(self, project_alias, srv_os, version, request_data):
        print(request_data)
        columns = self.filter_parameters(request_data.split(','))
        print(columns)
        query = self.get_data_by_columns(project_alias, srv_os, version, columns)
        print(query)

        with self.driver.session() as session: 
            result = session.run(query) 
            records = [record.data() for record in result] 
            return records

    def get_filtered_data_by_columns(self, project_alias, srv_os, version, columns, filters):
        columns_query = ", ".join(columns)
    
        # Construir la parte de MATCH dinámicamente según los parámetros
        match_clauses = [f"MATCH (Project:Project {{alias: '{project_alias}'}})"]
        if srv_os:
            match_clauses.append(f"MATCH (p)<-[:LINKED_TO]-(SrvOS:SrvOS {{srv_os: '{srv_os}'}})")
        if version:
            match_clauses.append(f"MATCH (s)<-[:LINKED_TO]-(Version:Version {{version: '{version}'}})")
        match_clauses.append("MATCH (Version)<-[:LINKED_TO]-(URL:URL)") 
        match_clauses.append("MATCH (URL)<-[:LINKED_TO]-(CVE:CVE)") 
        match_clauses.append("MATCH (CVE)<-[:LINKED_TO]-(Exploit:Exploit)")

        # Construir la parte de WHERE según los filtros proporcionados
        where_clauses = []
        for filter in filters.split(','):
            context, content = filter.split(':')
            where_clauses.append(f"{context} CONTAINS '{content}'")
        where_query = " AND ".join(where_clauses)

        # Unir todas las partes de la consulta
        query = "\n".join(match_clauses)
        if where_clauses:
            query += f"\nWHERE {where_query}"
        query += f"\nRETURN {columns_query}"
    
        return query

    def get_filtered_results(self, project_alias, srv_os, version, request_data, filters):
        columns = self.filter_parameters(request_data.split(','))
        print(f"FILTERED COLUMNS {columns}")
        query = self.get_filtered_data_by_columns(project_alias, srv_os, version, columns, filters)
        print(query)

        with self.driver.session() as session: 
            result = session.run(query) 
            records = [record.data() for record in result] 
            return records

import redis

class RedisManager:
    def __init__(self, host='vulnhunterai_redis_1', port=6379, db=0):
        self.host = host
        self.port = port
        self.db = db
        self.client = redis.StrictRedis(host=self.host, port=self.port, db=self.db, decode_responses=True)

    def save_value(self, key, value):
        try:
            self.client.set(key, value)
            print(f"Valor guardado en Redis: {key} = {value}")
        except redis.exceptions.RedisError as e:
            print(f"Error al guardar el valor en Redis: {e}")

    def get_value(self, key):
        try:
            value = self.client.get(key)
            if value is not None:
                print(f"Valor obtenido de Redis: {key} = {value}")
                return value
            else:
                print(f"No se encontró el valor para la clave: {key}")
                return None
        except redis.exceptions.RedisError as e:
            print(f"Error al obtener el valor de Redis: {e}")
            return None

    def delete_value(self, key):
        try:
            result = self.client.delete(key)
            if result:
                print(f"Valor eliminado en Redis: {key}")
            else:
                print(f"No se encontró el valor para eliminar: {key}")
        except redis.exceptions.RedisError as e:
            print(f"Error al eliminar el valor en Redis: {e}")
