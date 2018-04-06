# Managing and scaling Docker-ized data science apps

Although this CodeLab is a good chance to get yours hands dirty with Docker, there are whole books and courses on containers and related systems. The following sections attempt to expose you to some related topics that are relevant to data scientists using Docker.  

## Container Orchestration

Let's say that we love using Docker, and we containerize all of our things. Now we have a secondary problem of figuring out how we are going to manage all of those containers running across our infrastructure. It doesn't make much sense for data scientists and engineers to be ssh'ing into a bunch of machine and executing `docker run ...` commands all day.

Container orchestrators solve this problem. [Kubernetes](https://kubernetes.io/) is, by far, the leading container orchestration engine. With Kubernetes, you can declaratively specify that you want this many of container A, this many of container B, etc. running. Then Kubernetes will ensure that these things are are started and remain running on the underlying compute nodes (which could be cloud VMs or on-premise nodes).

## Managing Data ingress/egress, pipelines, and scaling

You may have noticed, as we went through our examples, that we still had to manually get data from one container to the next. This could turn into a giant, error-prone pain. Data and code in data science workflows are always changing, and we can rely on ourselves to get the right version of the right data to the right code at the right time on the right infrastructure.

[Pachyderm](http://pachyderm.io/) is a solution built on Kubernetes that solves these problems, while also allowing data scientists and AI researchers to scale their workloads (across both CPUs and GPUs). Pachyderm allows you to build data pipelines, where each stage of the data pipeline (e.g., training or inference) runs in a Docker container. Then, it will shim in data that you specify into the respective containers at the right time and in the right order. That way, you can focus on data sets and processing, and avoid spending all your time copying data and running containers. 

Pachyderm also versions all of your data and processing. This is super important for both compliance and maintenaince of workflows. With Pachyderm, you can always determine what data and processing contributed to a particular result, even if you have since changed the data sources and intermediate processing.

To get started with Pachyderm, take a look at their [getting started docs](http://pachyderm.readthedocs.io/en/latest/getting_started/getting_started.html) and join their [public Slack channel](http://slack.pachyderm.io/) to ask questions and get help.

## CI/CD

Often, Docker images that are used in production aren't built manually. Rather, the building (and sometimes running) or Docker images is integrated into a continuous integration/deployment pipeline (aka a CI/CD pipeline). 

CI/CD pipelines and systems automate the testing, building, and deployment process. These systems are often listening to your GitHub repos. When you push new code to certain branches (e.g., dev, staging, and prod), they will automatically pull your latest code, test that code, build a Docker image for your code, and deploy that Docker image (i.e., run it on) to some cloud or on-premise environment. 

Common tools used for CI/CD, and which integrate with Docker, are [Jenkins](https://jenkins.io/), [Travis](https://travis-ci.org/), [CircleCI](https://circleci.com/), and [Ansible](https://www.ansible.com/). Although there are many, many choices.
