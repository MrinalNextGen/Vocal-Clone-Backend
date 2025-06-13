# Vocal Clone - Backend API

This is the backend API for the Vocal Clone project, built with Python, Flask, and PostgreSQL. The entire environment is containerized with Docker for easy setup and deployment.

## ✨ Features

-   **RESTful API**: Full CRUD (Create, Read, Update, Delete) functionality for blogs.
-   **Database**: Uses PostgreSQL with SQLAlchemy for robust data management.
-   **Dockerized**: Comes with a `Dockerfile` and `docker-compose.yml` for a one-command setup.
-   **CORS Enabled**: Properly configured to allow requests from the frontend application.
-   **Environment Ready**: Uses a `.env` file for secure management of secrets and configuration.

## 🛠️ Tech Stack

-   **Framework**: Flask
-   **Database**: PostgreSQL
-   **ORM**: SQLAlchemy
-   **Containerization**: Docker, Docker Compose
-   **Language**: Python 3.11

## 🚀 Getting Started

### Prerequisites

-   [Docker](https://www.docker.com/products/docker-desktop/) and Docker Compose
-   [Git](https://git-scm.com/)

### 1. Clone the Repository

git clone https://github.com/MrinalNextGen/Vocal-Clone-Backend.git
cd Vocal-Clone-Backend



### 2. Configure Environment Variables

Create a `.env` file in the root of the backend folder and add the following configuration.

The database URL for connecting within the Docker network
DATABASE_URL=postgresql://vocal_user:your_db_password@db:5432/vocal_db

A strong, random secret key for Flask sessions
SECRET_KEY=your_super_secret_key_here


*Note: The `your_db_password` should match the `POSTGRES_PASSWORD` in your `docker-compose.yml` file.*

### 3. Run with Docker

This is the recommended method. From the project root (where `docker-compose.yml` is located), run:

docker-compose up --build


The API will be available at `http://localhost:5000`.

## 📝 API Endpoints

A brief overview of the available API endpoints:

| Method | Endpoint                     | Description                    |
| :----- | :--------------------------- | :----------------------------- |
| `GET`  | `/api/health`                | Checks the API and DB health.  |
| `GET`  | `/api/blogs`                 | Get a list of all blogs.       |
| `POST` | `/api/blogs`                 | Create a new blog post.        |
| `GET`  | `/api/blogs/<id>`            | Get a single blog by its ID.   |
| `PUT`  | `/api/blogs/<id>`            | Update an existing blog.       |
| `DELETE`| `/api/blogs/<id>`            | Delete a blog.                 |
| `PATCH`| `/api/blogs/<id>/favorite`   | Toggle a blog's favorite status.|
| `GET`  | `/api/blogs/favorites`       | Get all favorite blogs.        |


Run Your Fullstack App with Docker
1. Clone Your Repository
bash
git clone https://github.com/MrinalNextGen/vocal-clone.git
cd vocal-clone
2. Configure Environment Variables
Create .env in the backend folder (vocal-clone/backend/.env):

DATABASE_URL=postgresql://vocal_user:yourpassword@db:5432/vocal_db
SECRET_KEY=your-super-secret-key
3. Start All Services
bash
docker-compose up --build
This will:

Build backend (Flask) and frontend (React) images

Start PostgreSQL database

Create Docker network for inter-container communication

Migrate database schema automatically
## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.
