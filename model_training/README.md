# Docker-izing Model Training

To get some practice building Docker images for our data science apps (aka "Docker-izing" our data science apps), we are going to take the "Hello World" of machine learning as an example: the [Iris flower classification problem](https://en.wikipedia.org/wiki/Iris_flower_data_set).

Let's say that we have two Python applications that do the following, respectively:

- Train and save a model based on the Iris data set, and
- Utilize the trained model to perform inferences on new input attribtues of flowers.

First, we will Docker-ize the model training code, such that we can run it on any infrastructure with reproducible behavior. This guide will walk you through that process, which includes:

1. [Developing the application](README.md#1-developing-the-application)
2. [Creating a Dockerfile](README.md#2-creating-a-dockerfile)
3. [Building a Docker image](README.md#3-building-a-docker-image)
4. [Pushing the image to a registry (optional)](README.md#4-pushing-the-image-to-a-registry-optional)
5. [Running model training in a container](README.md#5-running-model-training-in-a-container)

Finally, I provide some [Resources](README.md#resources) for further exploration.

## 1. Developing the application

Because this isn't a Python CodeLab per se, I have already developed [a Python script (train.py)](train.py) that will perform this model training for you on the Iris dataset. The model will be capable of taking in a set of 4 measurements of a flower, and it will return a predicted species of that flower. 

The easiest way to continue the CodeLab with the prepared code to to clone this repo (or download the repo contents from [here](https://github.com/dwhitena/qcon-ai-docker-workshop)):

```sh
$ git clone https://github.com/dwhitena/qcon-ai-docker-workshop.git
```

Then you will be able to run the commands as presented below and modify the respective files. Of course, you are welcome to modify any of the included Python scripts to your liking (e.g., changing the modeling method). 

## 2. Creating a Dockerfile

To build a Docker image (that will allow us to run `train.py` in a container), we will need to create a Dockerfile. A Dockerfile tells Docker engine how a Docker image should be built. Think about this as a kind of recipe that Docker engine uses to build the image.

A basic Dockerfile for `train.py` is include [here](Dockerfile):

```
FROM python

# Install dependencies
RUN pip install -U numpy scipy scikit-learn pandas

# Add our code
ADD train.py /code/train.py
```

The Dockerfile format 

## 3. Building a Docker image

## 4. Pushing the image to a registry (optional)

## 5. Running model training in a container

## Resources
