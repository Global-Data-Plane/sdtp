'''
Unit tests for ServiceResolver, which turns a logical service_name into a
concrete URL depending on the deployment environment.
'''

import pytest

from sdtp.service_resolver import ServiceResolver
from sdtp.sdtp_utils import InvalidDataException


def test_docker_compose_default():
    resolver = ServiceResolver()
    assert resolver.resolve("people-service") == "http://people-service:8080"


def test_docker_compose_explicit():
    resolver = ServiceResolver()
    assert resolver.resolve("people-service", "docker-compose") == "http://people-service:8080"


def test_kubernetes():
    resolver = ServiceResolver()
    assert resolver.resolve("people-service", "kubernetes") == "http://people-service.default.svc.cluster.local:8080"


def test_cloud_run():
    resolver = ServiceResolver()
    assert resolver.resolve("people-service", "cloud-run") == "http://people-service:8080"


def test_unknown_deployment_raises():
    resolver = ServiceResolver()
    with pytest.raises(InvalidDataException, match="Unknown deployment type: bare-metal"):
        resolver.resolve("people-service", "bare-metal")
