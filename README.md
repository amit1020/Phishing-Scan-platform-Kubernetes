# Phishing-Scan-platform-Kubernetes

A web application that scans and detects phishing attempts using various tools. It provides a comprehensive solution to identify and mitigate phishing threats effectively.

## Table of Contents
- [Phishing-Scan-platform-Kubernetes](#phishing-scan-platform-kubernetes)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Features](#features)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
    - [Clone the Repository](#clone-the-repository)
    - [Using Docker-Compose](#using-docker-compose)
      - [Required Arguments for DockerImage](#required-arguments-for-dockerimage)
      - [Activation](#activation)
      - [Access the Application](#access-the-application)
  - [Usage](#usage)
  - [Folder Structure](#folder-structure)
    - [root folder](#root-folder)
    - [app\_data](#app_data)
    - [web folder](#web-folder)
      - [Explanation](#explanation)
    - [api files](#api-files)
        - [routes.py](#routespy)
  - [Contributing](#contributing)
  - [License](#license)
  - [Support](#support)
  - [Acknowledgements](#acknowledgements)

## Overview

Phishing Scan Platform analyzes phishing threats in a network, offering tools to identify and mitigate them effectively.

## Features

- Advanced phishing detection algorithms  
- Real-time analysis for suspicious activity  
- Intuitive web-based interface  
- Customizable alerts (email and more)  
- Comprehensive reporting  

## Prerequisites

- Python 3.8+  
- Docker  
- Docker Compose  

## Installation

### Clone the Repository

```bash
git clone https://github.com/amit1020/PhishingScanPlatform.git
cd PhishingScanPlatform
```

### Using Docker-Compose

#### Required Arguments for DockerImage

Provide these parameters as environment variables or command-line arguments:

- [API_VIRUSTOTAL](https://virustotal.com) 
- [API_URLSCAN](https://urlscan.io)
- REDIS_SECRET_KEY  
- REDIS_HOST  
- MYSQL_HOST  
- MYSQL_DATABASE  
- MYSQL_USER  
- MYSQL_PASSWORD  

#### Activation

```bash
docker-compose -f docker_compose.yml up --build
```

#### Access the Application

Go to [http://localhost:1234](http://localhost:1234).

## Usage

After deployment, the platform monitors phishing threats based on your configurations. Access the web interface to view alerts, generate reports, and manage settings.

## Folder Structure

### root folder

```plaintext
PhishingScanPlatform/
│── .github/
│── .vscode/
│── README_files/
│── app_data/
│── .dockerignore
│── docker_compose.yml
│── dockerfile
```

- `.github/workflows/`: GitHub Actions workflows  
- `README_files/`: Assets related to the README  
- `.dockerignore`: Files to ignore during Docker build  
- `docker_compose.yml`: Defines containers/services  
- `dockerfile`: Instructions to build the Docker image  

### app_data

```plaintext
app_data/
│── keys/
│── venv/
│── web/
├── .gitignore
├── app.py
├── requirements2.txt
├── wait-for-connection.sh
```

- `keys/`: Storage for keys  
- `venv/`: Python virtual environment  
- `web/`: Main application folder  
- `requirements2.txt` : This project requires certain Python packages to be installed. You can install them using:
```sh
pip install -r requirements2.txt
```

### web folder

```plaintext
web/
├── __init__.py
├── __pycache__/
├── admin/
├── api/
├── login_page/
├── Main_page/
```

#### Explanation

- `__init__.py`: Initializes the `web` package  
- `admin/`, `api/`, `login_page/`, `Main_page/`: Separate Blueprints with their own routes, static files, and templates  

### api files

```plaintext
api/
├── __init__.py               # Initializes 'api' as a Python package
├── routes.py                 # Defines routes/endpoints for the 'api' Blueprint
└── Functions_and_Classes/
    ├── __init__.py           # Imports and makes classes/functions available
    ├── Add_API.py            # Logic for adding API keys to the database
    ├── API_Class.py          # Classes that handle core API functionality
    ├── Database_class.py     # Database connection/interaction classes
    ├── General_Functions.py  # Helper/utility functions used by other modules
    ├── Users_DB.sql          # SQL script for creating/updating user DB tables
    └── __pycache__/          # Auto-generated compiled Python files
```

- `Add_API.py`: Reads and encrypts API keys before saving them to DB  
- `API_Class.py`: Manages core API functionality  
- `Database_class.py`: Database interaction logic  
- `General_Functions.py`: Common helper functions  
- `Users_DB.sql`
  
##### routes.py

  This file defines the routes for the `api` Blueprint in a Flask application. It includes the following key components:
  
  1. **Blueprint Definition**  
    - Defines the `API_bp` Blueprint with a prefix for all API endpoints.

  2. **Imports**  
    - Necessary modules and classes, such as `API_Helper`, `General_Functions`, and `Database_Connection_Class`.

  3. **Database Initialization**  
    - An instance of `Database_Connection_Class` is created for database interactions.

  4. **Routes**
    - **`/UserLogin/`**: Handles user login by verifying the username and password against the database.
    - **`/Vertification/2FA`**: Performs two-factor authentication by checking the provided OTP.
    - **`/add_user/`**: Adds a new user to the database after validating data and confirming the user doesn't already exist.
    - **`/ScanURL/`**: Scans a provided URL for potential phishing threats using external APIs and returns the results.

  5. **Helper Functions**
    - **`data_database_existence`**: Checks if specific user data already exists in the database.
    - **`is_ValidURL`**: Validates the format and reachability of a given URL.

  By organizing routes and their corresponding logic here, the application remains modular and easier to maintain.

## Contributing

Fork and submit a pull request with enhancements or fixes. Adhere to coding standards and include tests.

## License

This project is under the MIT License. See [LICENSE](LICENSE) for details.

## Support

Open an issue on GitHub or contact the maintainers directly.

## Acknowledgements

Thanks to all contributors and the open-source community for their support.
