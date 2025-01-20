# Usar una imagen base oficial de Python
FROM python:3.9-slim

RUN useradd -m user
RUN chown -R user:user /home

# Crea un directorio de trabajo
WORKDIR /home/user

USER user

# Configura el PATH para el usuario no-root
ENV PATH="$PATH:/home/user/.local/bin"

# Copiar el archivo de requisitos e instalar las dependencias
COPY requirements.txt /home/user/requirements.txt
COPY build.sh /home/user/build.sh
RUN pip install -r /home/user/requirements.txt

ENV PYTHONPATH='${PYTHONPATH}:/home/user'
ENV PYTHONUNBUFFERED=1

EXPOSE 5000

# Establecer las variables de entorno para Celery
ENV CELERY_BROKER_URL redis://redis:6379/0
ENV CELERY_RESULT_BACKEND redis://redis:6379/0

# Comando para iniciar celery_app.py y Celery en segundo plano
CMD ["/bin/bash", "-c", "/home/user/build.sh"]
