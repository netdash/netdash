## Deployment Strategies

### Simple: WSGI Server

A common deployment strategy is to copy or clone your NetDash project to a web server and serve it directly via WSGI.
Because NetDash integrates `whitenoise`, you can use `Gunicorn` to serve static content, circumventing the need for an additional web server such as `Apache` or `nginx`.

Pay attention to your deployed `settings.py`. For an example of how to configure NetDash's integrated SAML2 (Shibboleth) support, see `settings_env.py`.

Please see [Deploying Django](https://docs.djangoproject.com/en/2.2/howto/deployment/) for more information on deploying with this method. Pull requests with additional NetDash-specific deployment tips are welcome.

### Advanced: OpenShift/Kubernetes

An institution can deploy their own customized NetDash instance on Kubernetes by:
* Building and pushing a Docker image that extends a [NetDash Dockerhub image](https://hub.docker.com/r/netdash/netdash/tags).
* Creating [`kustomize`](https://kustomize.io/) overlays that extend [`netdash-k8s`](https://github.com/netdash/netdash-k8s).

This is the University of Michigan's preferred method of deploying NetDash. As an example, a high-level overview of the University of Michigan's build picture is as follows:

* Upon pushing a tag (such as `latest` or `beta` or `1.0.0`) to this repository, a CircleCI build is triggered which generates a corresponding [image on Dockerhub](https://hub.docker.com/r/netdash/netdash/tags). These public images can be used by any institution, and have not yet been customized for the University of Michigan.
* The University has a private GitLab repository with `kustomize` overlays (extending `netdash-k8s`) for UMich NetDash environments, as well as a `Dockerfile` for each environment, each extending Dockerhub NetDash images (e.g. `FROM netdash/netdash:beta`). These environment-specific Dockerfiles pull private NetDash Modules from an internal GitLab into the image and install them with `pip`. Developers clone this repository.
* On a developer's machine, secrets are copied from a secure store into the repository's `kustomize` overlay directories, e.g. `overlays/dev/secret`, which are gitignored.
* Kubernetes resources can be created and updated by running e.g. `kustomize build overlays/dev | oc apply -f -` from the developer's local repository.
* One of the created resources is an OpenShift Build. This Build, when triggered, builds environment-specific Docker images from the environment-specific Dockerfiles in the remote repository. It then pushes them to the OpenShift Image Registry, where they can be used by Deployments.
* Secret resources are also generated from the `overlays/dev/secret` directory, which the developer previously populated with secrets. Secrets become environment variables in OpenShift pods. NetDash can reference them through `settings_env.py`.

Additional automation can be achieved using GitLab/GitHub webhooks, OpenShift DeploymentConfig triggers, etc.
