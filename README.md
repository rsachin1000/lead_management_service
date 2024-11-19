# lead_management_service

Save sales leads and get a filtered list of leads

## Run the service

### Install dependencies

1. pip install -r requirements.txt
2. Start a `postgresql server` on localhost and then populate env variables in `.env` file.
3. Run the following to start the service:

```bash
$ python app/main.py
```

4. Use FastAPI docs service to test apis at `http://localhost:8080/docs`.

### Run on Docker

1. Build the docker image:

```bash
$ docker build -t fastapi-app .
```

2. Run the docker container:

```bash
$ docker run -d -p 8080:8080 fastapi-app
```

3. Note: if postgresql is also running on docker, then keep `DB_HOST=host.docker.internal`
