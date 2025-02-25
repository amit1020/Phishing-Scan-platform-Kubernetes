# Use the official Python image from Docker Hub
FROM python:3.11-slim

#Define args for the build
#ARG API_URLSCAN
#ARG API_virustotal
#ARG REDIS_SECRET_KEY
#ARG REDIS_HOST
#ARG MYSQL_HOST
#ARG MYSQL_DATABASE
#ARG MYSQL_USER
#ARG MYSQL_PASSWORD

#ENV API_URLSCAN=$API_URLSCAN \
#    API_VIRUSTOTAL=$API_VIRUSTOTAL \
#    REDIS_SECRET_KEY=$REDIS_SECRET_KEY \
#    REDIS_HOST=$REDIS_HOST \
#    MYSQL_HOST=$MYSQL_HOST \
#    MYSQL_DATABASE=$MYSQL_DATABASE \
#    MYSQL_USER=$MYSQL_USER \
#    MYSQL_PASSWORD=$MYSQL_PASSWORD



# Install MySQL client and netcat
RUN apt-get update && apt-get install -y --no-install-recommends \
    default-mysql-client netcat-openbsd openssl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
    
# Set working directory
WORKDIR /app

RUN mkdir /app/keys && \
openssl genpkey -algorithm RSA -out ./keys/Private.pem -pkeyopt rsa_keygen_bits:4096 && \
openssl rsa -in ./keys/Private.pem -pubout -out ./keys/Public.pem


RUN touch .env_api1 .env_app1 .user_db1






# Copy requirements and install dependencies
COPY ./app_data/requirements2.txt .
ENV PYTHONPATH="/app"
RUN pip install --no-cache-dir -r requirements2.txt

# Copy application files
COPY ./app_data/wait-for-connection.sh /app/wait-for-connection.sh
RUN chmod +x /app/wait-for-connection.sh

COPY ./app_data/ /app


    




# Run the application
CMD ["sh", "-c", "/app/wait-for-connection.sh phishing-scan-platform-db 3306 -- python app.py"]
