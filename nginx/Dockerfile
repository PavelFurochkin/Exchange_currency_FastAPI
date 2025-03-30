FROM nginx:latest

USER root


COPY nginx.conf /etc/nginx/conf.d/default.conf

COPY ./frontend /usr/share/nginx/frontend

CMD [ "nginx", "-g", "daemon off;" ]