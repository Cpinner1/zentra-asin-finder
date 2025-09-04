FROM node:20-alpine
WORKDIR /app
COPY web/package.json /app/package.json
RUN npm install
COPY web /app
RUN npm run build
EXPOSE 3000
CMD ["npm","start"]
