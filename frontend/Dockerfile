FROM oven/bun:1-alpine AS development-dependencies-env
COPY package.json bun.lock /app/
WORKDIR /app
RUN bun install

FROM node:20-alpine AS build-env
COPY . /app/
COPY --from=development-dependencies-env /app/node_modules /app/node_modules
WORKDIR /app
RUN npm run build

FROM node:20-alpine
COPY package.json /app/
WORKDIR /app
RUN npm install --production
COPY --from=build-env /app/build /app/build
EXPOSE 3000
CMD ["npm", "run", "start"]