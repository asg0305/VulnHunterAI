from flask import Flask, request, jsonify
import argparse
import threading
import sys
from Vulnhunter.execvuln.VulnHunterAI import VulnHunterAI
from config.output.output_config import OutputConfig

app = Flask(__name__)

@app.route('/process_data', methods=['POST'])
def process_data():
    data = request.json
    alias = data.get('alias')
    service = data.get('service')
    version = data.get('version')

    # Aquí procesarías los datos recibidos
    keywords = [alias, service, version]

    # Crear una instancia de VulnHunterAI y ejecutar el proceso de búsqueda en un hilo separado
    vuln_hunter_ai = VulnHunterAI('/home/user/resources/sites.json')
    search_thread = threading.Thread(target=vuln_hunter_ai.search_and_crawl, args=(keywords,))
    search_thread.start()

    return jsonify({"status": "success", "processed_data": f"Procesado el servicio {service} con versión {version}"})

def main():
    parser = argparse.ArgumentParser(description="VulnHunterAI - Herramienta para buscar vulnerabilidades y generar exploits.")
    parser.add_argument('keywords', type=str, nargs='+', help='Palabras clave (nombre del servicio o SO y versión)')
    args = parser.parse_args()

    keywords = args.keywords

    # Crear una instancia de VulnHunterAI
    vuln_hunter_ai = VulnHunterAI('/home/user/resources/sites.json')
    vuln_hunter_ai.search_and_crawl(keywords)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main()
    else:
        app.run(debug=True, host="0.0.0.0", port=5001)
