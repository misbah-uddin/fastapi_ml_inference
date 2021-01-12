# ML Inference using FastAPI

### Dependencies

See [requirements.txt](requirements.txt)

### Installation

The dependencies to run the codes are baked in a Docker container. 
To see how the container is created, check the [Dockerfile](Dockerfile).
To build the image run the following command:

```docker build -t housing .```

Test image by running the following command

```docker run -it housing python --version``` 

### Running

To launch a FastAPI server run the following command:

```docker run -it -p 8000:8000 -v ${PWD}:/opt/app housing uvicorn main:app --host 0.0.0.0 --reload```

A successful launch should show the following:

```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [1] using watchgod
INFO:     Started server process [9]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```
To test the API, send a POST request to the following URL

```http://localhost:8000/predict```


### Testing

