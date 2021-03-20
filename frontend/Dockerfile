FROM node:15.11.0-alpine

WORKDIR /app

ENV PATH /app/node_modules/.bin:$PATH

COPY package.json ./
COPY package-lock.json ./
RUN npm install --silent
RUN npm install react-scripts -g --silent
RUN npm install -g serve
RUN apk add bash
RUN apk add vim
RUN apk add curl

COPY ./build ./

CMD ["serve", "-s", "."]