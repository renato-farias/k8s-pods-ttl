import datetime

from freezegun import freeze_time

@freeze_time("2023-06-05 13:00:00 UTC")
def test_pod_ttl(pod_ttl):
    assert pod_ttl.phase == "Running"
    assert pod_ttl.start_time == datetime.datetime(2023, 6, 5, 12, 0, 0)
    assert pod_ttl.ttl_in_secs == 60
    assert pod_ttl.started_in_epoch == 1685962800
    assert pod_ttl.runtime_in_secs == 7200
    assert pod_ttl.due_to_rest

