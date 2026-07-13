'''
Tests for ContainerTable: a RemoteSDMLTable whose URL is resolved at
construction time from a logical service_name via ServiceResolver, rather
than being supplied directly.
'''

import pytest
from pytest_httpserver import HTTPServer

from sdtp import ContainerTable, InvalidDataException, SDML_NUMBER, SDML_STRING
from sdtp.sdtp_table_factory import TableBuilder
from sdtp.service_resolver import ServiceResolver


def _schema():
    return [
        {"name": "name", "type": SDML_STRING},
        {"name": "age", "type": SDML_NUMBER},
    ]


def _spec(service_name="people-service", env=None, table_name="test"):
    return {
        "type": "ContainerTable",
        "schema": _schema(),
        "table_name": table_name,
        "container": {"service_name": service_name, "env": env or {}},
    }


def test_container_table_resolves_docker_compose_url_by_default(monkeypatch):
    monkeypatch.delenv("SDTP_DEPLOYMENT", raising=False)
    table = TableBuilder.build_table(_spec())
    assert isinstance(table, ContainerTable)
    assert table.deployment == "docker-compose"
    assert table.url == "http://people-service:8080"
    assert not table.ok


@pytest.mark.parametrize(
    "deployment,expected",
    [
        ("docker-compose", "http://people-service:8080"),
        ("kubernetes", "http://people-service.default.svc.cluster.local:8080"),
        ("cloud-run", "http://people-service:8080"),
    ],
)
def test_container_table_resolves_url_per_deployment_env_var(monkeypatch, deployment, expected):
    monkeypatch.setenv("SDTP_DEPLOYMENT", deployment)
    table = TableBuilder.build_table(_spec())
    assert table.deployment == deployment
    assert table.url == expected


def test_container_table_unknown_deployment_raises(monkeypatch):
    monkeypatch.setenv("SDTP_DEPLOYMENT", "bare-metal")
    with pytest.raises(InvalidDataException, match="Unknown deployment type: bare-metal"):
        TableBuilder.build_table(_spec())


def test_container_table_legacy_aliases_still_resolve_url(monkeypatch):
    monkeypatch.delenv("SDTP_DEPLOYMENT", raising=False)
    legacy_spec = {
        "type": "ContainerTable",
        "schema": _schema()[:1],
        "name": "people",
        "computation": {"service_name": "legacy-service"},
    }
    table = TableBuilder.build_table(legacy_spec)
    assert table.table_name == "people"
    assert table.service_name == "legacy-service"
    assert table.env == {}
    assert table.url == "http://legacy-service:8080"


def test_container_table_connects_once_resolved(monkeypatch):
    '''
    ContainerTable delegates all data access to RemoteSDMLTable once its URL
    is resolved. Stand a local httpserver in for the container's SDTP
    endpoint by redirecting docker-compose resolution to it, then confirm
    connect_with_server behaves exactly as it does for a plain
    RemoteSDMLTable pointed at the same server.
    '''
    monkeypatch.delenv("SDTP_DEPLOYMENT", raising=False)
    httpserver = HTTPServer(port=8891)
    schema = _schema()
    monkeypatch.setattr(
        ServiceResolver,
        "_docker_compose_url",
        lambda self, service_name: httpserver.url_for("/"),
    )
    table = TableBuilder.build_table(_spec(table_name="test"))
    assert not table.ok

    httpserver.expect_request("/get_tables").respond_with_json({"test": schema})
    httpserver.start()
    try:
        table.connect_with_server()
        assert table.ok
    finally:
        httpserver.stop()


def test_container_table_bad_table_name_raises_once_resolved(monkeypatch):
    monkeypatch.delenv("SDTP_DEPLOYMENT", raising=False)
    httpserver = HTTPServer(port=8892)
    schema = _schema()
    monkeypatch.setattr(
        ServiceResolver,
        "_docker_compose_url",
        lambda self, service_name: httpserver.url_for("/"),
    )
    table = TableBuilder.build_table(_spec(table_name="not-there"))

    httpserver.expect_request("/get_tables").respond_with_json({"test": schema})
    httpserver.start()
    try:
        with pytest.raises(InvalidDataException, match="does not have table not-there"):
            table.connect_with_server()
        assert not table.ok
    finally:
        httpserver.stop()
