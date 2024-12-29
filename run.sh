#!/bin/bash
sudo docker exec -it vulnhunterai_container /bin/bash -c "rm -r /home/user/output/OnlineSearch/ && mkdir /home/user/output/OnlineSearch"
# Levantar el contenedor
sudo docker exec -it vulnhunterai_container /bin/bash -c "cd /home/user/Vulnhunter && python /home/user/Vulnhunter/main.py nuevo_alias nginx 0.1.5"
