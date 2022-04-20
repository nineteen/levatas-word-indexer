# Levatas Word Indexer

Levatas Word Indexer is a simple web crawler that will index the usage of words.

## Installation

Ths project uses [docker-compose](https://docs.docker.com/compose/) to manage the runtime environment and
[poetry](https://python-poetry.org/) to manage it's dependencies, although the latter should not be required for our
usage.

* Docker Installation Insturctions - https://docs.docker.com/get-docker/
* Docker Compose Installation Instructions - https://docs.docker.com/compose/install/
* Poetry Installation Instructions - https://python-poetry.org/docs/#installation



## Usage

Once you have docker and docker-compose installed correctly, you can start the environment with `docker-compose up -d`.
If this is your first time running the environment the docker-compose command will take care of building the docker images for you.
Below are a few other commands you might find helpful.

```bash
# Stopping the environment
docker-compose down

# Restarting the web server
docker-compose restart web

# Rebuilding the docker image
# Note: After rebuilding the image you will have to run docker-compose up -d
# again for the changes to take effect
docker-compose build

# Access the application logs
docker-compose logs web
```

Once the enivornment is up you can find the service running at http://localhost:8000.
Make sure you enter the full url you want to index into the url input. For example
`https://google.com` will work but `google.com` will not. The web page doesn't currently
handle error responses from the server, so if the service gets stuck, refresh the page.

The project also comes with a command line utility.
```bash
$ docker-compose exec web ./bin/indexer -h
usage: indexer [-h] [--print] url word

positional arguments:
  url         The url you want to index
  word        The word you want the count for

options:
  -h, --help  show this help message and exit
  --print     Print all of the words indexed and their count
```

## Contributing
All contributions should pass linting and contain unit and integration tests.
You can run the CI with the following commands.
```bash
# Run the code linting
docker-compose exec web pylint levatas_indexer

# Run the type checking
docker-compose exec web mypy levatas_indexer

# Run the unit tests
docker-compose exec web pytest tests/unit

# Run the integration tests
docker-compose exec web pytest tests/integration
```

## License
[MIT](https://choosealicense.com/licenses/mit/)
