FROM mediabox73/python-base:latest

RUN apt-get update


COPY . /var/www/
WORKDIR /var/www/

RUN pip install -r requirements.txt

EXPOSE 8000

ENTRYPOINT ["./docker-entrypoint.sh"]
