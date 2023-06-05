import pytest

from pod_ttl import PodTTL

@pytest.fixture()
def uid():
    return "02830796-6a87-4ee5-ae22-1e62720de276"


@pytest.fixture()
def name():
    return "pod-name-6c65d7988-bw6hr"


@pytest.fixture()
def namespace():
    return 'default'


@pytest.fixture()
def labels():
    return {
        "app": "my-app",
        "environment": "dev",
        "pod-template-hash": "6c65d7988"
    }


@pytest.fixture()
def annotations():
    return {
        "k8s-pods-ttl-enabled": "true",
        "k8s-pods-ttl-seconds": "60",
    }

@pytest.fixture()
def status():
    return {
        "phase": "Running",
        "startTime": "2023-06-05T12:00:00Z"
    }


@pytest.fixture()
def spec():
    return {}


@pytest.fixture()
def pod_ttl(uid, name, namespace, labels, annotations, status):
    return PodTTL(
        uid=uid,
        name=name,
        namespace=namespace,
        labels=labels,
        annotations=annotations,
        status=status
    )


