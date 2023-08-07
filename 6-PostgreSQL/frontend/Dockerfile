FROM node

WORKDIR /frontend

COPY package*.json /frontend/

RUN npm install

COPY . /frontend/

# RUN npm run build

# RUN npm install -g serve

EXPOSE 3000

CMD ["npm", "start"]