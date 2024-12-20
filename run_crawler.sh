#!/bin/bash

# Levantar el contenedor
sudo docker exec -it vulnhunterai_container /bin/bash -c "cd /home/user/Crawler && scrapy crawl nvd_spider -o /home/user/output/output.json"
