# Docker-izing Inference, Services

Now that we have our model training Docker-ized, we could run that model training on any Cloud or on-premise machines to produce a trained model. In addition to that, we might need to create a service (e.g., a REST API) that would allow us (or our users) to make requests for predictions, where our service would utilize the trained model to perform and serve the predictions. This guide will walk you through how you might develop, Docker-ize, and deploy this type of service: 

1. [Developing the application](README.md#1-developing-the-application)
2. [Creating a Dockerfile](README.md#2-creating-a-dockerfile)
3. [Building a Docker image](README.md#3-building-a-docker-image)
4. [Pushing the image to a registry (optional)](README.md#4-pushing-the-image-to-a-registry-optional)
5. [Running model inference as a service in a container](README.md#5-running-model-inference-as-a-service-in-a-container)

Finally, I provide some [Resources](README.md#resources) for further exploration.

## 1. Developing the application

Similar to model training, I have already developed the Python code we need for our desired functionality. Specifically, the [api.py script](api.py) will spin up an API (via flask) that will service model predictions. 

## 2. Creating a Dockerfile

A Dockerfile for `api.py` is included [here](Dockerfile):

```
FROM ubuntu

# install dependencies
RUN apt-get -y update --fix-missing && \
    apt-get install -y \
        python-pip \
        python-dev \
        libev4 \
        libev-dev \
        gcc \
        libxslt-dev \
        libxml2-dev \
        libffi-dev \
        python-numpy \
        python-scipy && \
    pip install --upgrade pip && \
    pip install scikit-learn flask-restful && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# add our project
ADD . /

# expose the port for the API
EXPOSE 5000

# run the API
CMD [ "python", "/api.py" ]
```

This Dockerfile is a little more complicated than the one we used for model training, but some things should look familiar. Everything in the arguments of the `RUN` instructions are things that you might run locally to prepare an environment to run our application. Note, how I have put a bunch of operations under a single `RUN` command. Why did I do this?

Well, remember how a Docker image is built up from "layers" that are versioned in a repository? If I put each of the `apt-get` or `pip` commands into separate `RUN` instructions, then those would build up more and more layers that would always be versioned with the Docker image. By combining them, I can perform some clean up at the end of all the installation (`rm -rf ...`) to get rid of cached info and other things I don't need. If the clean up was in a separate `RUN` instruction, it would basically have no effect on the overall size of the image.

Also, you will notice two new instructions in this Dockerfile that weren't in the model training Dockerfile:

- The `EXPOSE` instruction will expose a port in the container to be accessed from other running containers. Remember, we are going to make our predictions available via a call to an API, and it so happens that is API will be running on port 5000 in our container.
- The `CMD` instruction tells Docker that we want to run the provided command whenever the a container, based on this image, starts. The specific command here starts our prediction service using the `api.py` script. This is an alternative to manually specifying the command as we did with model training. 

## 3. Building a Docker image

We can now build our Docker image the same way we did for model training:

```sh
$ docker build -t <the name you choose> .
```

For example, to build the image such that I can push it up to my Docker Hub registry:

```sh
$ docker build -t dwhitena/model-inference:v1.0.0 .
```

## 4. Pushing the image to a registry (optional)

If desired you can also push the image to your Docker Hub registry (to version it and make it available on other systems):

```sh
$ docker push dwhitena/model-inference:v1.0.0
```

(where you would replace `dwhitena` with your Docker Hub username)

## 5. Running model inference as a service in a container

Now, to run this Python service in the container let's discuss briefly how we would run the code locally. This Python script is configured to be run as follows:

```sh
$ export MODEL_FILE=/path/to/this/GH/repo/model_training/data/model.pkl
$ python api.py
```

The `api.py` looks for an environmental variable `MODEL_FILE`, which should be set to location of the serialized model that was the output of our model training container. Once, that code is running, it will serve predictions on port 5000. For example, you could visit the following address in a browser (or via curl, postman, etc.) to get a prediction response in the form of JSON (assuming you are running the code locally):

```
http://localhost:5000/prediction\?slength\=1.5\&swidth\=0.7\&plength\=1.3\&pwidth\=0.3
``` 

When we run the code in the container, we will need to map the port 5000 inside of the container to a port outside of the container (such that we can use the service), map a volume with the `model.pkl` file into the container, and set the environmental variable `MODEL_FILE` in the container to specify the model file. Thus, to start the prediction service, run: 

```sh
$ docker run -v /path/to/this/GH/repo/model_training/data:/data -e MODEL_FILE='/data/model.pkl' -p 5000:5000 <your image tag>
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
```

where you would replace `<your image tag>` with the name of the Docker In this command:

- `-v /path/to/this/GH/repo/model_training/data:/data` maps the absolute path to the [data directory](../model_training/data) on your local machine to `/data` inside the container (remember we output our `model.pkl` file there). 
- `-e MODEL_FILE='/data/model.pkl'` sets the `MODEL_FILE` environmental variable in the container to the location of `model.pkl` in the container.
- `-p 5000:5000` maps port 5000 inside the container to port 5000 on our localhost. 

With this container running, you should be able to obtain a prediction from the service by visiting `http://localhost:5000/prediction\?slength\=1.5\&swidth\=0.7\&plength\=1.3\&pwidth\=0.3` in a browser (or via curl, postman, etc.). Try changing the `slength`, `swidth`, etc. parameters in the URL to get different predictions. Once you are done, you can remove the service via `CTRL+C`.

As excercises, look at the `docker run` reference docs to try and figure out how to:

- run the container in the background (i.e., non-interactively or as a daemon)
- after running the container in the background, open a bash shell in the running container from another terminal
- get the logs from the running container

Now that you are a pro at running your applications in Docker, see the next section of the CodeLab for some suggestions on how to automate ingress/egress of data, how to scale containerized workloads, and more.

## Resources

- [Docker run reference docs](https://docs.docker.com/engine/reference/run/)
- [Dockerfile reference docs](https://docs.docker.com/engine/reference/builder/)
