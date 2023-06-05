import logging
from unittest.mock import patch
from main import pod_to_delete


@patch("kubernetes.client.CoreV1Api")
def test_timer(k8s_core_v1_api, caplog, spec, uid, name, namespace, labels, annotations, status):
    caplog.set_level(logging.INFO)

    pod_to_delete(spec, uid, name, namespace, labels, annotations, status)
    assert caplog.record_tuples == [
        ("main", logging.INFO, "Pod pod-name-6c65d7988-bw6hr @ default UID: 02830796-6a87-4ee5-ae22-1e62720de276 is pending to be deleted."),
        ("main", logging.INFO, "Pod pod-name-6c65d7988-bw6hr @ default deleted.")
    ]

