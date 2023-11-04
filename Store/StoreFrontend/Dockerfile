FROM node:20

WORKDIR /usr/app

COPY ./yarn.lock ./
COPY ./package.json ./

RUN yarn

COPY . .

CMD [ "yarn", "dev" ]