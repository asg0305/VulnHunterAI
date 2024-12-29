# Usa una imagen base oficial
FROM python:3.9

# Crea un usuario no-root y establece permisos
RUN useradd -m user
RUN chown -R user:user /home

# Crea un directorio de trabajo
WORKDIR /home/user

# Cambia al nuevo usuario
USER user

#COPY requirements.txt .

# Instala las dependencias necesarias
#RUN pip install -r requirements.txt

# Configura el PATH para el usuario no-root
ENV PATH="$PATH:/home/user/.local/bin"

ENV PYTHONUNBUFFERED=1

RUN mkdir -p /home/user/SummAI_model

# Expone el puerto de la aplicación
EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["tail", "-f", "/dev/null"]
