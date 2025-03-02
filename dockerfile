# Use the official Python image from Docker Hub
FROM python:3.11-slim

#Define args for the build
# Define build arguments
ARG API_VIRUSTOTAL
ARG API_URLSCAN
ARG REDIS_SECRET_KEY
ARG REDIS_HOST
ARG MYSQL_HOST
ARG MYSQL_DATABASE
ARG MYSQL_USER
ARG MYSQL_PASSWORD
ARG MYSQL_ROOT_PASSWORD


# Convert ARG to ENV for runtime access
# Set environment variables using the ARG values
ENV API_VIRUSTOTAL=${API_VIRUSTOTAL} \
    API_URLSCAN=${API_URLSCAN} \
    REDIS_SECRET_KEY=${REDIS_SECRET_KEY} \
    REDIS_HOST=${REDIS_HOST} \
    MYSQL_HOST=${MYSQL_HOST} \
    MYSQL_DATABASE=${MYSQL_DATABASE} \
    MYSQL_USER=${MYSQL_USER} \
    MYSQL_PASSWORD=${MYSQL_PASSWORD} 

# Install MySQL client and netcat
RUN apt-get update && apt-get install -y --no-install-recommends \
    default-mysql-client netcat-openbsd openssl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
    
# Set working directory
WORKDIR /app

RUN mkdir /app/keys && \
openssl genpkey -algorithm RSA -out ./keys/Private.pem -pkeyopt rsa_keygen_bits:4096 && \
openssl rsa -in ./keys/Private.pem -pubout -out ./keys/Public.pem


RUN touch /app/.env_api  && \
    echo "virustotal=${API_VIRUSTOTAL}" >> /app/.env_api && \
    echo "urlscan=${API_URLSCAN}" >> /app/.env_api && \
    echo "SECRET_KEY=${REDIS_SECRET_KEY}" > /app/.env_app && \
    echo "REDIS_HOST=${REDIS_HOST}" >> /app/.env_app && \
    echo "MYSQL_HOST=${MYSQL_HOST}" > /app/.env_user_db && \
    echo "MYSQL_DATABASE=${MYSQL_DATABASE}" >> /app/.env_user_db && \
    echo "MYSQL_USER=${MYSQL_USER}" >> /app/.env_user_db && \
    echo "MYSQL_PASSWORD=${MYSQL_PASSWORD}" >> /app/.env_user_db #need to delete this when I use RDS


# Copy requirements and install dependencies
COPY ./app_data/requirements2.txt .
ENV PYTHONPATH="/app"
RUN pip install --no-cache-dir -r requirements2.txt

# Copy application files
COPY ./app_data/wait-for-connection.sh /app/wait-for-connection.sh
RUN chmod +x /app/wait-for-connection.sh

COPY ./app_data/ /app


# Run the application
CMD ["sh", "-c", "python app.py"]
