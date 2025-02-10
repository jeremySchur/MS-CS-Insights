# Get the base image
FROM node:20.18-alpine

# Set the working directory
WORKDIR /web

# Copy the package.json files
COPY package*.json .

# Install the dependencies
RUN npm install

# Copy the rest of the files
COPY . .

# Run the app
CMD ["npm", "run", "dev"]