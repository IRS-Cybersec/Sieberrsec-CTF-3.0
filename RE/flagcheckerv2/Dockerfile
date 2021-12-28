FROM nginx:alpine

COPY default.conf /etc/nginx/conf.d/default.conf
COPY ./html /usr/share/nginx/html/

RUN sed -i 's/}/    application\/wasm\t\t\t\t     wasm\;\n}/' /etc/nginx/mime.types
