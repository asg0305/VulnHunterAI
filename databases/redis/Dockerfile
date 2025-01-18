# Usar la imagen oficial de Redis desde Docker Hub
FROM redis:latest

RUN useradd -m user
RUN chown -R user:user /home

# Crea un directorio de trabajo
WORKDIR /home/user

# Exponer el puerto 6379 que es el puerto por defecto de Redis
EXPOSE 6379

CMD ["redis-server"]
