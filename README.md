# Media Box Events API

## Configuration file

TODO


## Running using Docker Compose

1. `$ export DOCKER_MOUNT=/path/to/docker-mount` Directory should contain the configuration files
1. `$ docker compose -f docker/docker-compose.yml build`
1. `$ docker compose -f docker/docker-compose.yml run -p 8001:8000 events bash` Running this command will bind port 8081 on the container to the host, and drop you into the container with the virtual environemnt activated.
1. `$ fastapi dev --host 0`
