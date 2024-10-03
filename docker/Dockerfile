FROM mediabox73/python-base:latest

#RUN apt-get update

WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /code

#EXPOSE 8000
#ENTRYPOINT ["./docker-entrypoint.sh"]
