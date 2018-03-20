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

Can you think of ways to make the image built from this Dockerfile smaller or more reproducible? A smaller image will mean it will download to target machine and initiate our work faster. It will also be easier to remove and update. Also, what happens if the `python` base image is updated? How can we keep this constant at a specific version? Try to create a modified version of the Dockerfile that:

- Utilizes a specific "tagged" version of the `python` base image,
- Utilizes a smaller version of the `python` base image, 
- Utilizes a different base image, and/or
- Cleans up other things in the image that aren't used.

## 3. Building a Docker image

Now that we have our Dockerfile, we can build our Docker image for model training. First, we need to choose a *tag* for our Docker image. For now, think of this tag as the name of the Docker image (although we will see that it has more utility later). 

To build our image, run the following from [this directory](.) in the cloned version of this repo:

```sh
$ docker build -t <the name you chose> .
```

The `-t <the name you chose>` argument tells Docker to tag your image as `<the name you chose>`, and the `.` at the end tells Docker to look for the Dockerfile in this directory. Note, you can also specify, via other flags, a Dockerfile in a different directory and/or a Dockerfile named something other than Dockerfile.

For example, I can create a `model-training` image by running:

```sh
$ docker build -t model-training .
Sending build context to Docker daemon  32.77kB
Step 1/3 : FROM python
latest: Pulling from library/python
f2b6b4884fc8: Pull complete
4fb899b4df21: Pull complete
74eaa8be7221: Pull complete
2d6e98fe4040: Pull complete
414666f7554d: Pull complete
135a494fed80: Pull complete
6ca3f38fdd4d: Pull complete
d67ff15d2a78: Pull complete
Digest: sha256:c021d6c587ea435509775c3a4da58d42287f630cb4ae6e0bc97ec839d9e0da3a
Status: Downloaded newer image for python:latest
 ---> d21927554614
Step 2/3 : RUN pip install -U numpy scipy scikit-learn pandas
 ---> Running in a77a8ec01d94
Collecting numpy
  Downloading numpy-1.14.2-cp36-cp36m-manylinux1_x86_64.whl (12.2MB)
Collecting scipy
  Downloading scipy-1.0.0-cp36-cp36m-manylinux1_x86_64.whl (50.0MB)
Collecting scikit-learn
  Downloading scikit_learn-0.19.1-cp36-cp36m-manylinux1_x86_64.whl (12.4MB)
Collecting pandas
  Downloading pandas-0.22.0-cp36-cp36m-manylinux1_x86_64.whl (26.2MB)
Collecting pytz>=2011k (from pandas)
  Downloading pytz-2018.3-py2.py3-none-any.whl (509kB)
Collecting python-dateutil>=2 (from pandas)
  Downloading python_dateutil-2.7.0-py2.py3-none-any.whl (207kB)
Collecting six>=1.5 (from python-dateutil>=2->pandas)
  Downloading six-1.11.0-py2.py3-none-any.whl
Installing collected packages: numpy, scipy, scikit-learn, pytz, six, python-dateutil, pandas
Successfully installed numpy-1.14.2 pandas-0.22.0 python-dateutil-2.7.0 pytz-2018.3 scikit-learn-0.19.1 scipy-1.0.0 six-1.11.0
You are using pip version 9.0.1, however version 9.0.2 is available.
You should consider upgrading via the 'pip install --upgrade pip' command.
Removing intermediate container a77a8ec01d94
 ---> 646a15f6e4df
Step 3/3 : ADD train.py /code/train.py
 ---> 3da96f640402
Successfully built 3da96f640402
Successfully tagged model-training:latest
```

You will notice in the output that Docker: pulls your base image, runs your commands to install dependencies, and then adds your code. The docker image will then be shown when you list the images in your local registry:

```sh
$ docker images
REPOSITORY                         TAG                 IMAGE ID            CREATED             SIZE
model-training                     latest              3da96f640402        3 minutes ago       1.21GB
dwhitena/minimal-jupyter           latest              1770383288b4        25 hours ago        203MB
python                             latest              d21927554614        3 days ago          688MB
tensorflow/tensorflow              latest              414b6e39764a        2 weeks ago         1.27GB
```

## 4. Pushing the image to a registry (optional)

One of the goals of Docker-izing our apps is to easily port them to other environments and make them available for other people to run. Thus, we can't be dependent on our laptop as the registry of our Docker images. We need to store and version our Docker images somewhere else (just like we would store and version our code somewhere like GitHub).

There are many options to choose from when thinking about where you want to store/version your images. You can also make your images public or keep them private (similar to having public/private repos on GitHub). Common choices for registries are [Docker Hub](https://hub.docker.com/), [AWS ECR](https://aws.amazon.com/ecr/), and [Google GCR](https://cloud.google.com/container-registry/). 

To get some practice, create a free user account on Docker Hub. Once you have done that, use the `docker login` command to log into your Docker Hub account locally. 

To push our `model-training` Docker image up to the Docker Hub registry as a public Docker image (that could be pulled down and run elsewhere), we first need to re-tag our image. Remember how we "named" our image `model-training`? Well, there's actually more utility in that tag than just a human readable name. We can tag our image with the format: `<registry, user>/<image name>:<version>`, where:

- `<registry, user>` specifies the registry and/or user associated with the image,
- `<image name>` specifies the common name of the image, and
- `<version>` specifies a version of the image.

For example, because I'm `dwhitena` on Docker Hub, I could tag my image as follows:

```sh
$ docker tag model-training dwhitena/model-training:v1.0.0
```

and then push it to Docker Hub:

```sh
$ docker push dwhitena/model-training:v1.0.0
The push refers to repository [docker.io/dwhitena/model-training]
dbd827af12d1: Pushed
eddb03e225ec: Pushed
aec4f1507d85: Mounted from library/python
a4a7a3673769: Mounted from library/python
325a22db58ea: Mounted from library/python
6e1b48dc2ccc: Mounted from library/python
ff57bdb79ac8: Mounted from library/python
6e5e20cbf4a7: Mounted from library/python
86985c679800: Mounted from library/python
8fad67424c4e: Mounted from library/python
v1.0.0: digest: sha256:ca5032522813f696c76e763becec0352f4765015536c6b1ff3f64a0e02898d30 size: 2427
```

Now v1.0.0 of my Docker image is available on Docker Hub [here](https://hub.docker.com/r/dwhitena/model-training/). Try this with your username and check that the image is pushed to Docker Hub.

**Note** - If you don't utilize a `:<version>` tag for your image (e.g., if I just used `dwhitena/model-training`), your image will be tagged as `latest`. This can be convenient while testing, but you should never use images tagged `latest` in production, because as you update the image you would lose the ability to revert to previous versions, run specific versions, etc.

## 5. Running model training in a container

Now, to run this Python model training code in the container let's discuss briefly how we would run the code locally. This Python script is configured to be run as follows:

```sh
$ python train.py <input directory> <output directory>
```

where `<input directory>` is the directory containing the iris training data set (included [here](data/iris.csv) in this repo) and `<output directory>` is where the Python script will save a serialized version of the trained model.

But how do we get the training data into our container? And how do we get the data out? Moreover, if our container finishes and we remove it, will we lose our data?

Well, Docker provides the ability to mount a "volume" into container. By mounting a local volume into the container, our container will be able to read data from the local filesystm and write data out to local filesystem. Then, once the container is deleted, we will still have the input/output data. We will use the `-v` flag with `docker run ...` to do this volume mapping.

From the root of this repo, you can run the model training in the container as follows:

```sh
$ docker run -v /path/to/this/GH/repo/model_training/data:/data <your image tag> python /code/train.py /data /data
```  

Where you would replace `<your image tag>` with the name of the Docker image you built in step 3 (`dwhitena/model-training:v1.0.0` in my case). `-v /path/to/this/GH/repo/model_training/data:/data` maps the absolute path to the [data directory](data) on your local machine to `/data` inside the container (you can use the `pwd` command to find the absolute path to that directory on your local machine). `python /code/train.py /data /data` is the command that we are running in the container to perform the training. 

This should only take a second to run. Once it finishes, you should see the model output in your `data` directory:

```sh
$ ls data
iris.csv  model.pkl model.txt
```

Yay! We successfully trained an ML model inside of a Docker container.

## Resources

- [Dockerfile reference](https://docs.docker.com/engine/reference/builder/)
- [Docker run reference](https://docs.docker.com/engine/reference/run/)
- [Docker volumes](https://docs.docker.com/storage/volumes/)
