# MS-CS-Insights

## Startup Guide

To get started with this project, follow these steps:

1. **Install Docker Desktop**:
   - Ensure Docker Desktop is installed on your machine. You can download it from [Docker's official website](https://www.docker.com/products/docker-desktop).

2. **Create a `.env` File**:
   - At the top level of the application folder, create a `.env` file.
   - Populate the `.env` file with the following configuration information:
     ```
      SLACK_TOKEN = your-slack-user-token

      VITE_BACKEND_API_URL = http://localhost:8000

      FRONTEND_URL = http://localhost:3000

      POSTGRES_USER = your-postgres-username
      POSTGRES_PASSWORD = your-postgres-password

      FRONTEND_PORT = 3000
      BACKEND_PORT = 8000
      POSTGRES_PORT = 5432
     ```

3. **Start the Application**:
   - Open a terminal and navigate to the Application directory.
   - Run the following command to start the application:
     ```sh
     docker-compose up
     ```
   - **Note**: The first docker-compose run may take time as it must download dependencies such as PyTorch.
    
4. **Access the Application**:
   - Once the application is running, you can access it by navigating to [http://localhost:3000](http://localhost:3000) in your browser.

**Note about the Database**:
   - You can hard reset the database by simply deleting the `/db` folder.

**Development Note**:
   - Currently, messages are being fetched from Slack every day. The reason for this is that if you fetch too often, replies to messages are often missed. A day interval should give messages enough time to gather replies before they are read.


