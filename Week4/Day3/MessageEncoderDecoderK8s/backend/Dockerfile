FROM node:18
WORKDIR /app
COPY package.json .
RUN npm install
COPY server.js .
EXPOSE 4000
CMD ["node", "server.js"]
