FROM node:20.18-alpine
WORKDIR /web
COPY package*.json .
RUN npm install
COPY vite.config.js .
COPY src src
CMD ["npm", "run", "dev"]