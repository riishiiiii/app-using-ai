
# Rishi Ki App

Welcome to the Rishi Ki App! This application allows users to register, login, write blogs, and view blogs. The frontend is built using HTML, CSS (TailwindCSS), and JavaScript, while the backend is powered by a FastAPI server.

## Prerequisites

Before you begin, ensure you have the following installed on your machine:

- Docker
- Docker Compose

## Getting Started

Follow these steps to get the application up and running using Docker Compose:

1. **Clone the repository:**

   ```sh
   git clone https://github.com/riishiiiii/app-using-ai.git
   cd app-using-ai
   ```

2. **Build and run the Docker containers:**

   ```sh
   docker-compose up --build
   ```

   This command will build the Docker images and start the containers for both the frontend and backend services.

3. **Access the application:**

   Once the containers are up and running, you can access the application in your web browser at:

   ```
   http://localhost:81
   ```

   The backend API will be available at:

   ```
   http://localhost:8000
   ```

## Project Structure

The project is organized as follows:

- `frontend/`: Contains the HTML, CSS, and JavaScript files for the frontend.
- `backend/`: Contains the FastAPI server code for the backend.
- `docker-compose.yml`: Docker Compose configuration file.

## Available Endpoints

### Authentication

- `POST /users/register`: Register a new user.
- `POST /users/login`: Login an existing user.

### Blog

- `POST /blog/write_blog`: Write a new blog post (requires authentication).
- `GET /blog/get_blogs`: Get all blog posts (requires authentication).
- `GET /blog/get_blog/{id}`: Get a specific blog post by ID.
- `DELETE /blog/delete_blog/{id}`: Delete a blog post by ID (requires authentication).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## Contact

If you have any questions or need further assistance, feel free to contact us at support@rishikiapp.com.

Enjoy using Rishi Ki App!
