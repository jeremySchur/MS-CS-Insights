# MS-CS-Insights

## Startup Guide

To get started with this project, follow these steps:

1. **Install Docker Desktop**:
    - Ensure Docker Desktop is installed on your machine. You can download it from [Docker's official website](https://www.docker.com/products/docker-desktop).

2. **Create a `.env` File**:
    - At the top level of the application folder, create a `.env` file.
    - Populate the `.env` file with the necessary configuration information. Refer to the project's documentation for the required variables.

3. **Start the Application**:
    - Open a terminal and navigate to the Application directory.
    - Run the following command to start the application:
      ```sh
      docker-compose up
      ```
   - **Note**: The first docker-compose run may take time as it must download dependencies such as PyTorch.
     
4. **Access the Application**:
   - Once the application is running, you can access it by navigating to [http://localhost:8080](http://localhost:8080) in your browser.

**Note about the Database**:
   - You can hard reset the database by simply deleting the `/db` folder.

