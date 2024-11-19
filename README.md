# lead_management_service

Save sales leads and get a filtered list of leads

## Run the service

### Install dependencies

1. Create a python virtual environment and install requirements: `pip install -r requirements.txt`.
2. `Postgresql server` is running on Supabase cloud. Credentials added to the .env file.
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

## Test the service

1. Deployed on Railway app. Please visit `https://leadmanagementservice-production.up.railway.app/docs`
