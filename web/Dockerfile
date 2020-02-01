## Remember to set the REACT_APP_API_URL 
## environment variable at build time and the 
## PORT environment variable at run time

FROM node:13

WORKDIR /container

# Install the static server that will serve the contents
RUN yarn global add serve

# Copy dependency list
ADD package.json .
ADD yarn.lock .

# Install dependencies
RUN yarn

# Get the code
ADD src ./src
ADD public ./public

# Require the API URI environment variable
# with some default value
ARG REACT_APP_API_URL=http://localhost:3456/api/v1.0.0/search

# Set the API URI environment variable & Build the react app
ENV REACT_APP_API_URL=$REACT_APP_API_URL
RUN yarn run build

CMD serve --listen $PORT --single build --no-clipboard