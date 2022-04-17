FROM node:16-alpine

WORKDIR /app
ADD app/package.json package.json

ENV NODE_PATH=node_modules
ENV PATH=$PATH:node_modules/.bin
RUN npm install

ADD app /app
ADD run.sh .

EXPOSE 3000
EXPOSE 35729

ENTRYPOINT ["/bin/sh", "/app/run.sh"]
CMD ["start"]
