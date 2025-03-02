FROM node:22.11.0-alpine
WORKDIR /web
COPY package*.json .
RUN npm install
COPY vite.config.js .
COPY public public
COPY src src
CMD ["npm", "run", "dev"]