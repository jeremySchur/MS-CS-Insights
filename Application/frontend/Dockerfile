# Get the base image
FROM node:20.18.0-bookworm-slim

# Set the working directory
WORKDIR /web

# Copy the package.json files
COPY package*.json .

# Install the dependencies
RUN npm install

# Copy the rest of the files
COPY . .

# Expose the port
EXPOSE 8080

# Run the app
CMD ["npm", "run", "dev"]