# ToDoList

Proyecto final del semillero 2022-3 de Devco.

Consiste en la creación de un API REST para la administración de una lista de to do. 

## Objetivos:
- Aplicación de arquitectura limpia.
- Contenerización (Docker).
- Pipeline de CI.
- Buenas prácticas de programación.
- Almacenamiento en BD.


## Comandos para la ejecución en local
1. Instalar requerimientos  
    ```
    pip install -r requirements.txt
    ```
2. Iniciar la base de datos
    ```
    flask --app src.adapters.app.application init-db
    ```
3. Comando la ejecutar la aplicación
    ```
    flask --app src.adapters.app.application --debug run -h 0.0.0.0 -p 8000
    ```

## Comando para construir la imagen de Docker local
1. Comando para construir la imagen
    ```
    docker image build -t flask_docker .
    ```
2. Comando para ejecutar el contenedor
    ```
    docker run -p 8000:8000 -d flask_docker
    ```

## Comando para construir contenedor Docker Hub
1. Comando para construir la imagen
    ```
    docker pull lauraisajb/tododevco
    ```
2. Comando para ejecutar el contenedor
    ```
    docker run -p 8000:8000 -d lauraisajb/tododevco
    ```

## Tecnologías utilizadas
- Python
- Flask
- Sqlite
- Docker
