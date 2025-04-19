FROM node:18-alpine
WORKDIR /app
COPY package.json ./
RUN npm install express aws-xray-sdk
COPY . .
EXPOSE 80
CMD ["node", "index.js"]
