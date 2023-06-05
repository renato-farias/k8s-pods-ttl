# k8s-pods-ttl

This Kubernetes operator deletes a pod when its TTL (time to live) set is reached forcing a new and fresh one to be created.

It uses [Kopf](https://github.com/nolar/kopf) which is a framework to build Kubernetes operators in Python.

The operator checks in a 60-second (hardcoded for time being) interval if the TTL for those Pods set was reached.


## Deploying

Create the service account and its permissions

> This can be too permissive as it only creates ClusterRole and ClusterRoleBinding, please check the permissions before running it in a production environment.


```bash
kubectl apply -f manifests/rbac.yaml
```


Deploy the operator

```bash
kubectl apply -f manifests/deployment.yaml
```

Now you need to specify in which deployments you want the operator to check and act when the TTL is reached. In order to do this, you need to set two annotations in your deployment under `spec/template/metadate/annotations`:

| Annotation | Value|
|---|---|
|k8s-pods-ttl-enabled| "true"|
|k8s-pods-ttl-seconds | "60" |

The exemple below shows how it should be:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-deployment
  namespace: default
  labels:
    app: my-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: my-deployment
  strategy:
    rollingUpdate:
      maxUnavailable: 0
  template:
    metadata:
      annotations:
        "k8s-pods-ttl-enabled": "true"
        "k8s-pods-ttl-seconds": "60"
```

## Developing

### Installing dependencies

```bash
poetry shell
poetry install
```

### Running the operator (It will use your default context to connect to a k8s Cluster, but running locally)

```bash
kopf run main.py
```

### Building the Docker Image

```bash
docker build -t k8s-pods-ttl .
```

### Running tests

```bash
make test
```
