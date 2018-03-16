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

## 3. Installing Docker

## 4. Interacting with Docker

## Resources

- [Getting started with Docker](https://docs.docker.com/get-started/)
- [Dockerfile reference](https://docs.docker.com/engine/reference/builder/)
