
Production
===========

The docker composition already bundles some powerful containers based on: Nginx, PostgreSQL, Redis, Celery, Django, Django REST Framework, Python and various related librairies. It thus provides a safe and continuous way to deploy your project from early development stages to more massive production environments.

Deploying
---------

First, create the ``env/prod.env`` and ``env/prod.yml`` files from the samples::

  cp env/prod.env.sample env/prod.env
  cp env/prod.yml.sample env/prod.yml

Then modify all the paths (especially for the data and media), passwords and secret keys in the two files.

Finally, setup the composition environment at the root of the project::

    echo "COMPOSE_FILE=docker-compose.yml:env/prod.yml" > .env


Scaling
--------

The Celery based worker container scales on all local CPUs automatically so that each processing pipelines is run asynchronously from its own thread. To scale on more machines, Kubernetes should offer evrything like demonstrated in these tutorials:

  - https://learnk8s.io/scaling-celery-rabbitmq-kubernetes
  - https://blog.devgenius.io/django-celery-in-kubernetes-for-scheduling-tasks-12718ef38bce

A Google Cloud based configuration is provided as an example in the ``k8s/`` directory.

