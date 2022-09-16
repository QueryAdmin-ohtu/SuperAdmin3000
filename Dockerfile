# This Python package should include most dependencies for our purposes.
FROM python:3.10-slim-bullseye
# Install curl and netcat => Install poetry
RUN pip install -U pip \
    && apt-get update \
    && apt install -y curl netcat \
    && curl -sSL https://install.python-poetry.org | python3 -
# Set PATH enviromental variable to enable bash commands as e.g. '$ poetry version'
ENV PATH="${PATH}:/root/.local/bin"
# Application work directory inside container as per convention:
WORKDIR /usr/src/app
# Copy configuraiton files for '$ poetry install' before copying the rest of the repository to container for caching purposes
COPY poetry* .

COPY pyproject.toml .
# Check poetry installation and that the PATH enviromental variable works properly:
RUN poetry version
# Install project dependencies utilising poetry as usual. Changes above this line result in a more expensive '$ docker build' operation.
RUN poetry install
# Now we can copy the repository files to the container.
COPY . .
# Now, set database env variables, expose the required ports and so forth!
EXPOSE 5000
# Finally, this CMD starts up the application
CMD [ "poetry", "run", "invoke", "start"]

### The application should be running now:
#   The command 
#     $ sudo docker container ls -a
#   Should return something like
#     CONTAINER ID   IMAGE                COMMAND                  CREATED              STATUS                        PORTS                                       NAMES
#     9503e80ac8fe   olenleo/superadmin   "poetry run invoke s…"   About a minute ago   Up About a minute             0.0.0.0:5000->5000/tcp, :::5000->5000/tcp   tender_volhard
#   Access a container shell with the following:
#       $ sudo docker exec -it tender_volhard bash
#     Now, inside container, the command
#       root@9503e80ac8fe:/usr/src/app# curl http://127.0.0.1:5000
#     ... should return the application!
#     <title>SuperAdmin3000</title> etc
