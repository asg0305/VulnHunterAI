#!/bin/bash

# Levantar el contenedor
sudo docker exec -it vulnhunterai_container /bin/bash -c "cd /home/user/Vulnhunter && scrapy crawl nvd_crawler"
