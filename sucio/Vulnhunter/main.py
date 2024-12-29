import argparse
#from spiders.vuln_spider import VulnSpider
#from summarizer.summarizer import Summarizer
from VulnHunterAI import VulnHunterAI
from config.output.output_config import OutputConfig
import subprocess

def llamar_script_ejecutar_spiders():
    script = 'exec_scrapy.py'
    comando = ['python', script]
    print(f'Ejecutando script: {script}')
    resultado = subprocess.run(comando, capture_output=True, text=True)
    print(f'Salida del script:\n{resultado.stdout}')
    if resultado.stderr:
        print(f'Error en el script:\n{resultado.stderr}') 


def main():
    parser = argparse.ArgumentParser(description="VulnHunterAI - Herramienta para buscar vulnerabilidades y generar exploits.")
    parser.add_argument('keywords', type=str, nargs='+', help='Palabras clave (nombre del servicio o SO y versión)')
    args = parser.parse_args()

    keywords = args.keywords

    # Crear una instancia de VulnHunterAI
    # vuln_hunter_ai = VulnHunterAI('/home/user/resources/sites.json')
    # vuln_hunter_ai.search_and_crawl(keywords)
    llamar_script_ejecutar_spiders()

if __name__ == "__main__":
    main()
