# Usar una imagen base oficial de Python
FROM python:3.9-slim

RUN useradd -m user
RUN chown -R user:user /home

# Crea un directorio de trabajo
WORKDIR /home/user

USER user

# Configura el PATH para el usuario no-root
ENV PATH="$PATH:/home/user/.local/bin"
ENV PYTHONPATH='${PYTHONPATH}:/home/user'
ENV PYTHONUNBUFFERED=1

# Copiar el archivo de requisitos e instalar las dependencias
COPY requirements.txt /home/user/requirements.txt
RUN pip install --no-cache-dir -r /home/user/requirements.txt

# Copiar el archivo celery_app.py
COPY celery_app.py /home/user/celery_app.py

EXPOSE 5000

# Establecer las variables de entorno para Celery
ENV CELERY_BROKER_URL redis://redis:6379/0
ENV CELERY_RESULT_BACKEND redis://redis:6379/0

# Comando para iniciar celery_app.py y Celery en segundo plano
CMD ["/bin/bash", "-c", "python /home/user/celery_app.py & cd /home/user/backend && celery -A tasks worker --loglevel=info"]
