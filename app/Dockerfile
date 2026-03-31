FROM python:3.11-alpine

# Installation des dépendances système nécessaires pour MySQL et Docker SDK
RUN apk add --no-cache gcc musl-dev mariadb-connector-c-dev pkgconfig

WORKDIR /app

# Installation des dépendances Python
# flask, flask-sqlalchemy, pymysql, docker, cryptography
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5003

# Copie du code source
COPY app/ .

# Exécution du microservice
CMD ["python", "app.py"]
