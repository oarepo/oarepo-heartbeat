import json

from flask import current_app

from oarepo_heartbeat import environ_probe, liveliness_probe, readiness_probe


def readiness():
    data = [x[1] for x in readiness_probe.send()]
    return _collect_results(*data)


def liveliness():
    data = [x[1] for x in liveliness_probe.send()]
    return _collect_results(*data)


def environ():
    data = {}
    total_status = True
    for x in environ_probe.send():
        status, values = x[1]
        total_status &= status
        data.update(values)
    return current_app.response_class(json.dumps({
        'status': total_status,
        **data
    }))


def _collect_results(*values):
    total_status = True
    checks = {}
    for name, status, data in values:
        total_status &= status
        checks[name] = {
            **data,
            'status': status
        }
    return current_app.response_class(json.dumps({
        'status': total_status,
        'checks': checks
    }), status=200 if total_status else 500)
