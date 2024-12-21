import argparse
#from spiders.vuln_spider import VulnSpider
#from summarizer.summarizer import Summarizer
from Vulnhunter.execvuln.VulnHunterAI import VulnHunterAI
from config.output.output_config import OutputConfig

def main():
    parser = argparse.ArgumentParser(description="VulnHunterAI - Herramienta para buscar vulnerabilidades y generar exploits.")
    parser.add_argument('keywords', type=str, nargs='+', help='Palabras clave (nombre del servicio o SO y versión)')
    args = parser.parse_args()

    keywords = args.keywords

    # Crear una instancia de VulnHunterAI
    vuln_hunter_ai = VulnHunterAI('/home/user/resources/sites.json')
    vuln_hunter_ai.search_and_crawl(keywords)

if __name__ == "__main__":
    main()
