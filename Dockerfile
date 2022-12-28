########### BACKEND REQUIREMENTS ###################
FROM python:3.10-slim as requirements-stage

WORKDIR /tmp
RUN pip install poetry
COPY ./pyproject.toml ./poetry.lock* /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes --dev

########### BACKEND ###################
FROM python:3.10-slim as backend

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# set work directory
WORKDIR /app

# install dependencies
RUN pip install --upgrade pip
COPY --from=requirements-stage /tmp/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./backend /app

########### BACKEND DEBUGGER ###################
FROM backend as backend_debug
RUN pip install debugpy

WORKDIR /app

########### FRONTEND DEVELOPMENT ###################
FROM node:16.14-alpine3.15 as frontend_dev

WORKDIR /app
COPY ./frontend/package.json ./frontend/yarn.lock  ./

RUN yarn install

COPY ./frontend ./

RUN yarn build

########### FRONTEND PRODUCTION ###################
FROM nginx:1.21-alpine as frontend_prod

RUN rm -rf /usr/share/nginx/html/* && rm /etc/nginx/conf.d/default.conf
COPY ./nginx.conf /etc/nginx/conf.d
COPY --from=frontend_dev /app/dist /usr/share/nginx/html

EXPOSE 80

ENTRYPOINT ["nginx", "-g", "daemon off;"]




