FROM node

WORKDIR /frontend

COPY package*.json /frontend/

RUN npm install

COPY . /frontend/

RUN npm run build