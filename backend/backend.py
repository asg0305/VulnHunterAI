from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process_input():
    data = request.json
    alias = data.get('alias')  # Obtener el alias del JSON recibido
    service = data.get('service')
    version = data.get('version')

    # Enviar datos al tercer contenedor mediante POST
    third_container_url = "http://vulnhunterai_container:5001/process_data"
    response = requests.post(third_container_url, json={'service': service, 'version': version, 'alias': alias})  # Incluir alias en la solicitud
    prueba = request.get("http://localhost:4444/app.txt")

    if response.status_code == 200:
        return jsonify({"status": "success", "data": response.json()})
    else:
        return jsonify({"status": "error", "message": "Failed to process data in third container"}), 500

if __name__ == "__main__":
    print("Starting Flask server...")
    app.run(debug=True, host="0.0.0.0", port=5000)
