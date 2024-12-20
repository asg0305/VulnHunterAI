import requests
import sys

def fetch_url_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Verifica si la solicitud fue exitosa (código 200)
        content = response.text
        print(content)
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener la URL: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python fetch_url_content.py <URL>")
        sys.exit(1)
    
    url = sys.argv[1]
    fetch_url_content(url)

