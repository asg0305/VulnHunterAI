#!/bin/bash

# Levantar el contenedor
sudo docker exec -it vulnhunterai_container /bin/bash -c "python /home/user/main.py nuevo_alias nginx 0.1.5"
