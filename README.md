# Proyecto de Preguntas y Respuestas con Flask, Docker, Tomcat y MySQL

Este proyecto es una aplicación web que permite a los usuarios enviar preguntas y obtener respuestas generadas por el modelo GPT-3.5-turbo de OpenAI. La aplicación está desarrollada con Flask y utiliza Docker para la gestión de contenedores, Tomcat para servir una página HTML, y MySQL (MariaDB) para la base de datos.

## Contenido

- `docker-compose.yml`: Configuración de Docker Compose para ejecutar los contenedores de Tomcat y Flask.
- `flask_app/app.py`: Código fuente de la aplicación Flask.
- `flask_app/Dockerfile`: Archivo Docker para construir la imagen de la aplicación Flask.
- `flask_app/requirements.txt`: Archivo de requisitos para la aplicación Flask.
- `mariadb/init.sql`: Script SQL para inicializar la base de datos.
- `tomcat/Dockerfile`: Archivo Docker para construir la imagen de Tomcat.
- `tomcat/webapps/ROOT/index.html`: Página HTML servida por Tomcat.

## Requisitos Previos

- Docker y Docker Compose instalados en tu sistema.
- Una clave de API de OpenAI.

## Instrucciones

### 1. Configurar la Base de Datos

Crea una base de datos MySQL (MariaDB) y una tabla para almacenar las preguntas y respuestas, así como una tabla de configuración para almacenar la clave de API de OpenAI:

```sql
CREATE TABLE IF NOT EXISTS questions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    response TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS configuration (
    id INT AUTO_INCREMENT PRIMARY KEY,
    config_key VARCHAR(255) NOT NULL,
    config_value TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```


### 2. Ejecutar la Aplicación desde Cero
```
git clone https://github.com/sirtxo/QuestionGenieGPT
cd QuestionGenieGPT
````

```
docker-compose up --build
```

```
sql INSERT INTO configuration (config_key, config_value) VALUES ('openai_api_key', 'tu-clave-de-api-aqui');
```

 ###License
```
This project is licensed Free.
 ```
