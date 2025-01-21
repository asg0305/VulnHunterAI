# VULNHUNTERAI
### Despliegue de la herramienta
```bash
git clone https://github.com/asg0305/VulnHunterAI
cd VulnHunterAI
docker-compose up -d
```

https://github.com/user-attachments/assets/abc03aac-e646-49c1-8ceb-7bf8bf734385


### Acceso a la herramienta
- **Panel de ejecución**: localhost:8050
- **Base de datos Neo4j**: localhost:7687 (neo4j:password)


https://github.com/user-attachments/assets/18400813-91a9-4c03-b7d5-3cc9f46edcf5





### ¿Qué es VulnHunterAI?

VulnHunterAI es una herramienta de búsqueda de vulnerabilidades para servicios y sistemas operativos. Su objetivo es facilitar la búsqueda de exploits y vulnerabilidades realizada por los pentesters durante la fase de análisis. Aunque actualmente es un pequeño POC debido a limitaciones de búsqueda online, el objetivo es continuar mejorando y ampliando las capacidades de la herramienta para automatizar gran parte de la búsqueda online en el contexto del pentesting.

### Proceso de búsqueda

La primera versión de la herramienta consta de un panel principal donde el usuario introduce un alias para la búsqueda, un servicio o sistema operativo y su versión. Posteriormente, se realiza una petición al backend donde se sigue el siguiente proceso:
1. **Generación de dorks** para una búsqueda precisa. *(Google dorking permite encontrar información específica mediante consultas avanzadas en motores de búsqueda).*
2. **Búsqueda online** mediante la biblioteca `googlesearch` o `yagooglesearch`.
3. **Crawling de las páginas web** con `scrapy`.

Finalmente, se mostrarán los resultados al usuario mediante una tabla interactiva que permite el filtrado de contenido y atributos.

### Estructura interna

La estructura interna del proyecto se divide en tres partes principales:

1. **Base de datos Neo4j**: Se emplea para guardar la trazabilidad de los servicios, versiones y vulnerabilidades encontradas. Se puede acceder mediante el navegador en `localhost:7474` con las credenciales `neo4j/password` para ver el contenido completo de la base de datos. Actualmente, su utilidad es almacenar estas relaciones, clave para que en el futuro, cuando se incluya en otra herramienta con IA, puedan usarse como base de datos para entrenar el modelo.

2. **Backend de la aplicación**: Es el núcleo de la herramienta. Recibe el input del usuario y da comienzo a las tareas de ejecución. Destacar que, para el uso de `scrapy`, ha sido necesario implementar su ejecución mediante `celery`, debido a la gestión de hilos de ejecución.

3. **Base de datos Redis**: Es una base de datos almacenada en memoria y en la que se apoya `celery` para su ejecución. Permite una ejecución asíncrona del resto de tareas y un acceso más rápido a los datos.


### Limitaciones

Uno de los mayores retos al desarrollar este proyecto ha sido evitar la detección como bot por Google. Se ha decidido optar por dos implementaciones distintas:

- La primera implementación funcionaría al inicio si Google no detecta como bot el dispositivo. Emplea la biblioteca `googlesearch`.
- La segunda, en cambio, hace uso de la biblioteca `yagooglesearch`, ya que permite la búsqueda mediante el uso de proxies. Estos deben ser configurados por el usuario en el fichero `proxies.py` del directorio `OnlineSearch`. Debido a la configuración de la biblioteca, solo es funcional con proxies de NA, pero se espera actualizarla para la UE próximamente.

Para cambiar el uso de una a otra es necesario comentar y descomentar las bibliotecas importadas en el archivo `tasks`. Además, dicho archivo contiene URLs de pruebas que permiten comprobar que el crawling web funciona.

### Uso de Inteligencia Artificial

En las próximas versiones más avanzadas de este proyecto, se intentará hacer uso de IA para generar exploits acorde a cada búsqueda indicada por el usuario. En el panel de resultados, el usuario ya puede obtener el enlace a los exploits registrados para dicha vulnerabilidad. Sería interesante poder introducir dicho exploit en una IA sin restricciones para, de esta forma, ofrecer el exploit adaptado al contexto o parámetros indicados por el usuario.
