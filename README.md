## Flask restful API

Designing a RESTful API using Flask

## Docker

```sh
docker build -t restful_contacts:latest .
docker run --rm --name docker-flask -p 5000:8000 restful_contacts
```

This will create the image and pull in the necessary dependencies.

Once done, run the Docker image and map the port to whatever you wish on
your host. In this example, we simply map port 5000 of the host to port 8000 of the Docker


## Pipenv

```sh
pipenv run app
pipenv run test
```
