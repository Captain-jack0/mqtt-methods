FROM node:16-alpine
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm install --production
COPY index.js ./
CMD ["node", "index.js"]

