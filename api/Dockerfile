FROM node:13

WORKDIR /container

COPY package.json .
COPY yarn.lock .
RUN yarn install

COPY src .

CMD [ "yarn", "start" ]