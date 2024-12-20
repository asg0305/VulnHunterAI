#!/bin/bash
sudo docker-compose down -v
sudo docker stop $(sudo docker ps -aq)
sudo docker rm $(sudo docker ps -aq)
sudo docker rmi $(sudo docker images -aq)
sudo docker-compose up -d
sudo docker exec -it vulnhunterai_container  /bin/bash -c "pip install networkx twisted scrapy transformers torch requests googlesearch-python Flask==2.0.2 requests==2.25.1"
sudo docker exec -it vulnhunterai_container /bin/bash -c "python -c \"from transformers import BartTokenizer, BartForConditionalGeneration; BartTokenizer.from_pretrained('facebook/bart-large-cnn', cache_dir='/home/user/SummAI_model'); BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn', cache_dir='/home/user/SummAI_model')\""
#sudo docker exec -it vulnhunterai_container /bin/bash -c "python -c \"cd /home/user && scrapy Crawler\"

# Construir la imagen Docker
#sudo docker build -t vulnhunterai_image .

# Levantar el contenedor con el montaje del volumen correcto
#sudo docker run -it --rm --name vulnhunterai_container -p 8000:8000 -v "$(pwd):/app" vulnhunterai_image
