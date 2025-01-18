"""
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

from googlesearch import search
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

def search_and_fetch(query):
    try:
        # Realiza una búsqueda en Google utilizando Google Dorks
        resultados = list(search(query, num_results=5))  # Obtiene los primeros 5 resultados
        print(resultados)
        # Verifica si hay resultados
        for url in resultados:
            print(f"URL encontrada: {url}")
            fetch_url_content(url)
    except Exception as e:
        print(f"Error durante la búsqueda en Google: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python search_and_fetch.py <consulta_de_búsqueda>")
        sys.exit(1)
    
    query = sys.argv[1]
    search_and_fetch(query)
"""
try:
    from googlesearch import search
except ImportError: 
    print("No module named 'google' found")


import requests
from bs4 import BeautifulSoup
import sys

def fetch_url_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Verifica si la solicitud fue exitosa (código 200)
        content = response.text
        print(content)
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener la URL: {e}")

def search_with_dorks(query):
    url = f"https://www.google.com/search?q={query}"
    
    # Establecemos las cabeceras para la solicitud HTTP
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Verifica si la solicitud fue exitosa (código 200)

        # Analizamos el contenido de la página
        soup = BeautifulSoup(response.text, "html.parser")

        # Buscamos todos los enlaces de los resultados de búsqueda
        resultados = []
        for g in soup.find_all('div', class_='yuRUbf'):
            link = g.find('a')['href']
            resultados.append(link)
        
        if resultados:
            for resultado in resultados:
                print(f"URL encontrada: {resultado}")
                fetch_url_content(resultado)
        else:
            print("No se encontraron resultados.")
    except requests.exceptions.RequestException as e:
        print(f"Error durante la búsqueda en Google: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python search_with_dorks.py <consulta_de_búsqueda>")
        sys.exit(1)
    
    query = sys.argv[1]
    search_with_dorks(query)
