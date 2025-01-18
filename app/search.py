import requests
from bs4 import BeautifulSoup

query = "recetas de cocina saludables"
url = f"https://www.google.com/search?q={query}"

# Establecemos las cabeceras para la solicitud HTTP
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

# Realizamos la solicitud HTTP
response = requests.get(url, headers=headers)

# Analizamos el contenido de la página
soup = BeautifulSoup(response.text, "html.parser")

# Buscamos todos los enlaces de los resultados de búsqueda
for g in soup.find_all('div', class_='BNeawe vvjwJb AP7Wnd'):
    print(g.get_text())
