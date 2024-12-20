import scrapy
import networkx as nx
from AI.summ_ai import SummAI
import json
from resources.keywords import search_keywords

class VulnSpider(scrapy.Spider):
    name = "vuln_spider"
    
    def __init__(self, start_urls, keywords, *args, **kwargs):
        super(VulnSpider, self).__init__(*args, **kwargs)
        self.start_urls = start_urls
        self.keywords = keywords
        self.extra_keywords = search_keywords
        self.max_depth = 2
        self.summ_ai = SummAI()  # Inicializar SummAI
        self.results = []  # Lista para almacenar los resultados
        self.key_in_url = []  # Lista para URLs que contienen palabras clave
        self.key_in_content = []  # Lista para contenido que contiene palabras clave
        self.graph = nx.DiGraph()  # Grafo dirigido
        self.analyzed_urls = set()  # Conjunto para rastrear URLs ya analizadas
        self.url_depths = {}  # Diccionario para rastrear la profundidad de cada URL
        print(f"VulnSpider initialized with start_urls: {start_urls} and keywords: {keywords}")

    def start_requests(self):
        print("Starting requests")
        for url in self.start_urls:
            print(f"Sending request to: {url}")
            self.url_depths[url] = 0  # Inicializar la profundidad de las URL iniciales
            yield scrapy.Request(url, self.parse)

    def parse(self, response):
        # Verificar si el código de respuesta es 200
        print(f"Processing URL: {response.url}")
        if response.status == 200:
            content = response.text
            summary = self.summ_ai.summarize(content)

            # Añadir nodo al grafo
            self.graph.add_node(response.url, summary=summary)

            # Buscar palabras clave en la URL y el contenido
            found_in_url = any(keyword in response.url for keyword in self.extra_keywords)
            found_in_content = any(keyword in content for keyword in self.extra_keywords)

            # Guardar la URL en la lista correspondiente
            if found_in_url:
                self.key_in_url.append(response.url)
            if found_in_content:
                self.key_in_content.append(response.url)

            result = {
                'url': response.url,
                'summary': summary,
                'found_in_url': found_in_url,
                'found_in_content': found_in_content
            }
            self.results.append(result)
            print(f"Processed URL: {response.url} with summary: {summary}")

            # Guardar resultados en archivo JSON
            with open('results.json', 'w') as f:
                json.dump(self.results, f, indent=4)
            with open('key_in_url.json', 'w') as f:
                json.dump(self.key_in_url, f, indent=4)
            with open('key_in_content.json', 'w') as f:
                json.dump(self.key_in_content, f, indent=4)

        """
        # Extraer enlaces y seguirlos (si es necesario)
        current_depth = self.url_depths.get(response.url, 0)
        if current_depth < self.max_depth:
            links = response.css('a::attr(href)').extract()
            for link in links:
                full_link = response.urljoin(link)
                # Evitar reanalizar URLs ya vistas
                if full_link not in self.analyzed_urls:
                    self.analyzed_urls.add(full_link)
                    self.url_depths[full_link] = current_depth + 1
                    self.graph.add_edge(response.url, full_link)  # Añadir arista al grafo
                    print(f"Following link: {full_link}")
                    yield response.follow(full_link, self.parse)

        # Guardar grafo en formato JSON compatible con Cytoscape
        cyto_graph = nx.cytoscape_data(self.graph)
        with open('graph.json', 'w') as f:
            json.dump(cyto_graph, f, indent=4)
        """