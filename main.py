import asyncio
import logging
from typing import Any, Mapping
from dataclasses import dataclass
import kopf
import kubernetes

from pod_ttl import PodTTL

logger = logging.getLogger(__name__)

def delete_pod(name, namespace):
    k8s_pod_v1 = kubernetes.client.CoreV1Api()
    k8s_pod = k8s_pod_v1.delete_namespaced_pod(
        name=name,
        namespace=namespace)
    logger.info(f"Pod {name} @ {namespace} deleted.")

@kopf.timer('pods', interval=60, annotations={"k8s-pods-ttl-enabled": "true"})
def pod_to_delete(spec, uid, name, namespace, labels, annotations, status, **kwargs):
    pod_ttl = PodTTL(
        uid=uid,
        name=name,
        namespace=namespace,
        labels=labels,
        annotations=annotations,
        status=status
    )
    logger.debug(f"Pod Name: {pod_ttl.name}")
    logger.debug(f" started_in_epoch: {pod_ttl.started_in_epoch}")
    logger.debug(f" runtime_in_secs: {pod_ttl.runtime_in_secs}")
    logger.debug(f" ttl_in_secs: {pod_ttl.ttl_in_secs}")
    logger.debug(f" due_to_rest: {pod_ttl.due_to_rest}")

    if pod_ttl.due_to_rest:
        logger.info(
            f"Pod {pod_ttl.name} @ {pod_ttl.namespace} "
            f"UID: {pod_ttl.uid} is pending to be deleted."
        )
        delete_pod(pod_ttl.name, pod_ttl.namespace)
