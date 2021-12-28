FROM alpine:3.14
EXPOSE 23547

ENV PYTHONUNBUFFERED=1
RUN apk add --update --no-cache python3 py3-pip

WORKDIR /root
COPY src/ /root/
RUN pip3 install -r /root/requirements.txt

CMD python3 main.py
