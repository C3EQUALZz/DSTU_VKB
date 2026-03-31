FROM node:20-alpine AS build

WORKDIR /app

COPY frontend/package.json /app/package.json
RUN npm install

COPY frontend /app

ARG VITE_API_BASE_URL=/api/v1
ARG VITE_HEALTH_URL=/health
ENV VITE_API_BASE_URL=${VITE_API_BASE_URL}
ENV VITE_HEALTH_URL=${VITE_HEALTH_URL}

RUN npm run build

FROM nginx:1.27-alpine

COPY deploy/frontend.nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
