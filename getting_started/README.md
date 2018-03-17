# Getting started with Docker

Ideally, we should be creating ML applications that produce preditable behavior, regardless of where they are deployed. [Docker](https://www.docker.com/) can be utilized to accomplish this goal. 

The below sections help you understand why Docker is useful in this context and some of the jargon associated with Docker. It will also walk you through installation and basic use of Docker:

1. [Why Docker?](README.md#1-why-docker)
2. [Docker Jargon](README.md#2-docker-jargon)
3. [Installing Docker](README.md#3-installing-docker)
4. [Interacting with Docker](README.md#4-interacting-with-docker)

Finally, I provide some [Resources](README.md#resources) for further exploration.

## 1. Why Docker?

Ok, let's say that we have some code for model training, inference, pre-processing, post-processing, etc. and we need to:

- scale this code up to larger data sets,
- run it automatically at certain times or based on certain events, 
- share it with teammates so they can generate their own results, or
- connect it to other code running in our company's infrastructure.

You aren't going to be able to do these things if your code only lives on your laptop and if you have to run it manually in your own environment. You need to *deploy* this code to some other computing resources and/or share it such that others can run it just like you. This other environment could be one or more cloud instances or an on premise cluster of compute nodes. 

How can we do this with a high degree of reproducibility and operational/computation efficiency? And how can we ensure that our engineering team doesn't hate the data science team because they always have to deploy data science things in a "special" way with "special" data science tools. 

Well, some of you might be thinking that Virtual Machines (or VMs) are the answer to this problem. To some degree you are correct. VMs were developed to solve some of these issues. However, many have moved on from VMs because they create quite a few pain points:

- They generally consume a fixed set of resources. This makes it hard to take advantage of computational resources in an optimized way. Most of the time VMs aren't using all of the resources allocated to them, but we have partitioned those resources off from other processes. This is waste.
- Most of the time they are pretty big. Porting around a 10Gb VM image isn't exactly fun, and I wouldn't consider it incredibly "portable."
- If you are running applications in the cloud, you can run into all sorts of weirdness if you try to run VMs inside of VMs (which is what cloud instances actually are).

Docker solves many of these issues and even has additional benefits because it leverages *software containers* as it primary way of encapsulating applications. Containers existed before Docker, but Docker has made containers extremely easy to use and accesible. Thus many just associate software containers with Docker containers. When working with Docker containers, you might see some similarities to VMs, but they are quite different:

![Alt text](https://blog.netapp.com/wp-content/uploads/2016/03/Screen_Shot_2016-03-11_at_9.14.20_PM1.png)

As you can see Docker containers have the following unique properties which make them extremely useful:

- They don't include an entire guest OS. They just include your application and the associated libraries, file system, etc. This makes them much smaller than VMs (some of my Docker containers are just a few Mb). This also makes spinning up and tearing down containers extremely quick.
- They share an underlying host kernel and resources. You can spin up 10s or 100s or Docker containers on a single machine. They will all share the underlying resources, such that you can efficiently utilize all of the resources on a node (rather than statically carving our resource per process). 

This is why Docker containers have become so dominant in the infrastructure world. Data scientists and AI researchers are also latching on to these because they can:

- Docker-ize an application quickly, hand it off to an engineering organization, and have them run it in a manner similar to any other application.
- Experiment with a huge number of tools (Tensorflow, PyTorch, Spark, etc.) without having to install anything other than Docker.
- Manage a diverse set of data pipeline stages in a unified way.
- Leverage the huge number of excellent infrastructure projects for containers (e.g., those powering Google scale work) to create application that auto-scale, self-heal, are fault tolerant, etc.
- Easily define and reproduce environments for experimentation.

## 2. Docker Jargon

Docker jargon can sometimes be confusing, so let's go ahead and define some key terms. Refer back to this list later on the CodeLab if you need to:

- Docker *Image* - the bundle that includes your app & dependencies
- Docker *Container* - a running instance of a Docker image
- *Docker engine* - the application that builds and runs images
- Docker *registry* - where you store, tag, and get pre-built Docker images
- *Dockerfile* - a file that tells the engine how to build a Docker image

Thus, a common workflow when building a Docker-ized application is as follows:

1. Develop the application (as you normally would)
2. Build a Docker image for the app with Docker engine
3. Upload the image to a registry
4. Deploy a Docker container, based on the image from the registry, to a cloud instance or on premise node

## 3. Installing Docker

Docker can be installed on Linux, Mac, or Windows. If you are using Windows, note that I will be showing unix-style commands throughout the CodeLab. As such, you may want to run command from the the WSL or look up the Windows command prompt equivalents.

To install Docker (the community edition), following the appropriate guide [here](https://www.docker.com/community-edition#/download). Once installed, you should be able to run the following in a terminal to get the Docker version:

```sh
$ docker version
Client:
 Version:	17.12.0-ce
 API version:	1.35
 Go version:	go1.9.2
 Git commit:	c97c6d6
 Built:	Wed Dec 27 20:03:51 2017
 OS/Arch:	darwin/amd64

Server:
 Engine:
  Version:	17.12.0-ce
  API version:	1.35 (minimum version 1.12)
  Go version:	go1.9.2
  Git commit:	c97c6d6
  Built:	Wed Dec 27 20:12:29 2017
  OS/Arch:	linux/amd64
  Experimental:	true
```

**Note** - in some cases, you may need to run any `docker ...` commands as `sudo`. This should be fine for this CodeLab, but, if you want to be able to run without `sudo`, you could follow [this guide](https://docs.docker.com/install/linux/linux-postinstall/). 

## 4. Interacting with Docker

Once you have Docker installed, you can manage, build, and run Docker images from the command line. To see what images you have locally, you can run:

```sh
$ docker images
REPOSITORY                         TAG                 IMAGE ID            CREATED             SIZE
dockerized-test                    latest              6fa518ef72d2        2 hours ago         607MB
ubuntu                             latest              f975c5035748        9 days ago          112MB
```

You might not have any images yet, because you haven't pulled any. Let's go ahead and pull a Docker image from Docker's public registry called [DockerHub](https://hub.docker.com/) (think of it like GitHub but for Docker images):

```sh
$ docker pull dwhitena/minimal-jupyter
Using default tag: latest
latest: Pulling from dwhitena/minimal-jupyter
550fe1bea624: Already exists
b313ba46199e: Already exists
de349a63b77a: Already exists
3cd0781adeaa: Already exists
0cf242809b69: Pull complete
4a2fb11c3300: Pull complete
Digest: sha256:893107a7f4e27e772460aeddea0626bd1196aba9b0cc6468d3f52c47ff369e03
Status: Downloaded newer image for dwhitena/minimal-jupyter:latest
```

Now, when you list your docker images with `docker images` this image will show up in your local registry of images (because we pulled it from the remote registry).  This `dwhitena/minimal-jupyter` image (as you might have guessed from the name) is a docker image that includes Jupyter. Even if you don't have Jupyter, ipython, etc. installed locally, you can use Jupyter via this Docker image by running it:

```sh
$ docker run -p 8888:8888 dwhitena/minimal-jupyter
[I 20:47:17.087 NotebookApp] Writing notebook server cookie secret to /home/jovyan/.local/share/jupyter/runtime/notebook_cookie_secret
[W 20:47:18.403 NotebookApp] WARNING: The notebook server is listening on all IP addresses and not using encryption. This is not recommended.
[W 20:47:18.403 NotebookApp] WARNING: The notebook server is listening on all IP addresses and not using authentication. This is highly insecure and not recommended.
[I 20:47:18.421 NotebookApp] Serving notebooks from local directory: /home/jovyan/notebooks
[I 20:47:18.421 NotebookApp] 0 active kernels
[I 20:47:18.421 NotebookApp] The Jupyter Notebook is running at:
[I 20:47:18.421 NotebookApp] http://[all ip addresses on your system]:8888/
[I 20:47:18.422 NotebookApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
```

As you can see (if you are familiar with Jupyter), this command started a Jupyter notebook server. However, the server isn't running directly on your localhost. It is running inside of a Docker container based on the `dwhitena/minimal-jupyter` Docker image. To see this, open a new terminal window and run `docker ps` to see what containers are running:

```sh
$ docker ps
CONTAINER ID        IMAGE                      COMMAND                  CREATED             STATUS              PORTS                    NAMES
55803aae3021        dwhitena/minimal-jupyter   "/bin/sh -c 'jupyter…"   2 minutes ago       Up 2 minutes        0.0.0.0:8888->8888/tcp   cranky_sinoussi
```

Try visiting `localhost:8888` in your browser to see the Jupyter notebook server running in the Docker container!

There are quite a variety of options that you can specify when running your Docker containers. We specified `-p 8888:8888` above, which mapped port 8888 inside the container (where Jupyter is running) to port 8888 outside of the container. However, we could have also specified a name for the container, run the container as a daemon, changed the container's networking, and much more. For a full list and explaination of these options see the [docker run reference docs](https://docs.docker.com/engine/reference/run/).

To stop this running container, you can run `docker rm -f <container ID>` from the terminal where you ran `docker ps`. Or you should be able to close it via `CTRL + C` in the terminal where you ran the `docker run` command. 

**Note** - You could recreate this process on any machine in the cloud or on premise, as long as that machine has Docker installed. You wouldn't have to install the right version of Jupyter, ipython, etc. You just need to `docker run`. In fact, you can `docker run` TensorFlow, PyTorch, R, ggplot, Postgres, MongoDB, Spark, or whatever you want, without messing with any dependencies. That's awesome! Hopefully, you are beginning to see the power and flexibility of containers. 

## Resources

- [Getting started with Docker](https://docs.docker.com/get-started/)
- [Dockerfile reference](https://docs.docker.com/engine/reference/builder/)
