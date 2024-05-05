# Ecommerce Platform

This project is an e-commerce platform designed to provide APIs for e-commerce websites, both for customers and sellers. It includes a frontend for customers to browse products and make purchases, along with authentication using JWT tokens. The backend includes APIs for managing products, orders, and user authentication.

## Features

1. APIs for e-commerce websites for customers and sellers.
2. Frontend provided for customers.
3. Authentication using JWT tokens.
4. Database safeguarded against injection attacks.
5. Deployment simplified using Docker.

## Contents

- [Installation](#installation)
- [Usage](#usage)
- [Deployment](#deployment)

## Installation

1. Clone the frontend and backend repositories into a folder:
 ```
 git clone https://github.com/sameerksingh/ecommerce-ui
 git clone https://github.com/sameerksingh/ecommerce-api
 ```

2. Install Docker Compose:
```
# For Linux
sudo apt install docker-compose

# For macOS
brew install docker-compose
```

3. Add a file docker-compose.yml with the following contents:
```
version: '3'

services:
  frontend:
    build: ./ecommerce-ui
    ports:
      - "8080:8080"

  backend:
    build: ./ecommerce-api
    ports:
      - "5000:5000"
    environment:
      - MONGO_URI=mongodb://mongodb:27017/
    depends_on:
      - mongodb

  mongodb:
    image: mongo:latest
    ports:
      - "27017:27017"
```

4. Run the following command to start the services:
```
docker-compose up
```

This will start the frontend, backend, and MongoDB services using Docker Compose.

## Usage

After installation, you can access the frontend at http://localhost:8080 and the backend at http://localhost:5000.
To connect to the MongoDB instance, use the following connection string: mongodb://localhost:27017/

## Deployment

This app can be easily deployed on an aws server under free tier, for example on an EC2 Amazon linux instance t2-micro device.


