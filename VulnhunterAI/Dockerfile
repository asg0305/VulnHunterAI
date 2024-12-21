# Usa una imagen base oficial
FROM python:3.9

# Crea un usuario no-root y establece permisos
RUN useradd -m user
RUN chown -R user:user /home

# Crea un directorio de trabajo
WORKDIR /home/user

# Cambia al nuevo usuario
USER user

# Copia el archivo de requisitos
#COPY requirements.txt .

# Instala las dependencias necesarias
#RUN pip install -r requirements.txt

RUN mkdir -p /home/user/SummAI_model

# Descargar los modelos durante el build
#RUN python -c "from transformers import BartTokenizer, BartForConditionalGeneration; \
#                BartTokenizer.from_pretrained('facebook/bart-large-cnn', cache_dir='/home/user/SummAI_model'); \
#                BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn', cache_dir='/home/user/SummAI_model')"

# Configura el PATH para el usuario no-root
ENV PATH="$PATH:/home/user/.local/bin"

# Comando para mantener el contenedor en ejecución
CMD ["tail", "-f", "/dev/null"]
