# Media Box Events API

## Configuration file

TODO


## Running using Docker Compose

1. `$ docker compose up -d`

## Running using Docker Compose for dev
1. `$ docker compose run -it api bash` Running this command will bind port 8081 on the container to the host, and drop you into the container.
2. `$ python manage.py api dev` - will run API in development mode
3. `$ docker compose run -it listener bash`
4. `$ python manage.py listen` - will run kafka listeners
