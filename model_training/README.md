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

The Dockerfile format includes a series of *instructions* (in all caps) paired with corresponding *arguments*. Each of the *instructions* will result in a *layer* in the Docker image. The Docker image is generated and versioned in layers, such that you can easily change your code without having to rebuilt the image from scrath. It also allows us to build on others work as well. For example, we don't have to build up an Ubuntu like file and packaging system or install python (although we could). We can just say `FROM python`. 

If you are looking for public images (like `python` above) that you can start from, try [Docker Hub](https://hub.docker.com/). For example, if you search for "TensorFlow" in Docker Hub you will find a `tensorflow/tensorflow` image that is maintained by the TensorFlow team (along with many other TF images maintained by other people). There are scikit-learn, caret, ggplot, PyTorch, Spark, and many other public images that will allow you to experiment and create Docker images quickly.

**Warning** - Although searching Docker Hub is a good place to start when you need a base image for a Dockerfile, not all images published to Docker Hub are operation, secure, or ideal. Just like pulling code and packages from GitHub, you should investigate who is publishing the image, when it was last updated, and if it is created in a sane manner. For example, there are a bunch of base "data science" images on Docker Hub that include a whole ecosystem of data science tooling (jupyter, scikit-learn, TF, PyTorch, etc.). I highly recommend that you avoid these type of images (unless you just want to experiment with them locally). For the most part, they are super bloated (like > 1GB in size) and hard to work with, download, port, etc. At that point you might as well use a full VM. haha. 

**Continued Warning** - Even images published by known teams are sometimes non-ideal. For example, the "minimal" Jupyter notebook image from the Jupyter team is over 1GB in size, which is hardly minimal (the one we pulled is 72MB). Generally a large image size, lack of documentation, non-public Dockerfile, and lack of recent updates are bad signs when looking for a base image.

Ok, with that soapbox out of the way, let's look at the other two layers of our Dockerfile. The second instruction (`RUN ...`) tells Docker to install numpy, scipy, scikit-learn, and pandas on top of python. We will need these to run our training. Note, there are public images with scikit-learn etc. already installed, but these include a bunch of other things that we don't need. As such, it makes sense for us to just start from `python` and add in the few things we need.

Finally, we need to add our code to the image, the `ADD ...` instruction tells Docker to add `train.py` to the `/code/train.py` location in the image.   

## 3. Building a Docker image

## 4. Pushing the image to a registry (optional)

## 5. Running model training in a container

## Resources
