import sys
import argparse
import subprocess

def main():
    parser = argparse.ArgumentParser(description="Ejecutar spiders de Scrapy con parámetros personalizados.")
    parser.add_argument('spider_name', type=str, help='El nombre del spider que deseas ejecutar.')
    parser.add_argument('file_path', type=str, help='La ruta al archivo JSON con las URLs.')
    
    args = parser.parse_args()

    # Crear el comando
    comando = f'scrapy crawl {args.spider_name} -a file_path={args.file_path}'

    # Ejecutar el comando usando subprocess
    resultado = subprocess.run(comando, shell=True, capture_output=True, text=True)
    print(f'Salida del script:\n{resultado.stdout}')
    if resultado.stderr:
        print(f'Error en el script:\n{resultado.stderr}')

if __name__ == "__main__":
    main()
