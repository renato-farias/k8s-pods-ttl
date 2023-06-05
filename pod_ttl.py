import logging
import datetime
from typing import Any, Mapping
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class PodTTL:
    uid: str
    name: str
    namespace: str
    labels: Mapping[str, Any]
    annotations: Mapping[str, Any]
    status: Mapping[str, Any]
    phase: str = None
    start_time: datetime.datetime = None

    def __post_init__(self):
        logger.debug(f"New PodTTL instance created: {self}")
        self.phase = self.status.get("phase")
        self.start_time = datetime.datetime.strptime(
            self.status.get("startTime"),
            "%Y-%m-%dT%H:%M:%SZ")

    @property
    def started_in_epoch(self):
        return int(self.start_time.astimezone(tz=datetime.timezone.utc).timestamp())

    @property
    def runtime_in_secs(self):
        return int(datetime.datetime.utcnow().timestamp()) - self.started_in_epoch

    @property
    def ttl_in_secs(self):
        return int(self.annotations.get("k8s-pods-ttl-seconds"))

    @property
    def due_to_rest(self):
        return self.runtime_in_secs >= self.ttl_in_secs
