# Usa una imagen base oficial
FROM python:3.9

# Crea un directorio de trabajo
WORKDIR /app

# Copia el archivo de requisitos
COPY requirements.txt .

# Instala las dependencias necesarias
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto de la aplicación
EXPOSE 8050

# Comando para ejecutar la aplicación
CMD ["python", "app.py"]
