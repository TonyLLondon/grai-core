import pathlib
import tempfile
import uuid

import yaml
from grai_cli.api.entrypoint import app
from grai_cli.api.server.endpoints import apply, delete, get_edges, get_nodes
from grai_cli.utilities.test import prep_tests
from grai_cli.utilities.utilities import write_yaml
from typer.testing import CliRunner

prep_tests()
runner = CliRunner()


def make_v1_node():
    node = {
        "version": "v1",
        "type": "Node",
        "spec": {
            "name": "name-" + str(uuid.uuid4()),
            "namespace": "namespace-" + str(uuid.uuid4()),
            "data_source": "test",
        },
    }
    return node


def make_v1_edge(source_id, destination_id):
    node = {
        "version": "v1",
        "type": "Edge",
        "spec": {
            "data_source": "tests",
            "source": source_id,
            "destination": destination_id,
            "name": "name-" + str(uuid.uuid4()),
            "namespace": "test",
        },
    }
    return node


def test_apply_single_node():
    file = tempfile.NamedTemporaryFile("w+")
    file_name = pathlib.Path(file.name)
    node_dict = make_v1_node()
    write_yaml(node_dict, file_name)
    result = runner.invoke(app, ["apply", file.name])
    assert result.exit_code == 0, result


def test_apply_multi_node():
    file = tempfile.NamedTemporaryFile("w+")
    file_name = pathlib.Path(file.name)
    nodes = [make_v1_node() for i in range(5)]
    write_yaml(nodes, file.name)
    result = runner.invoke(app, ["apply", file.name])
    assert result.exit_code == 0


def test_create_and_get_nodes():
    with tempfile.NamedTemporaryFile("w+") as file:
        nodes = [make_v1_node() for i in range(2)]
        write_yaml(nodes, file.name)
        result = runner.invoke(app, ["apply", file.name])
        assert result.exit_code == 0
        server_nodes = get_nodes(print=False)
        node_set = {(str(n.spec.name), str(n.spec.namespace)) for n in server_nodes}
        original_node_set = {(n["spec"]["name"], n["spec"]["namespace"]) for n in nodes}
        diff = original_node_set - node_set
        assert len(diff) == 0, "Created nodes were not returned by get"


def test_delete_single_node():
    file = tempfile.NamedTemporaryFile("w+")
    file_name = pathlib.Path(file.name)
    node_dict = make_v1_node()
    yaml.dump(node_dict, file)
    result = runner.invoke(app, ["apply", file.name])
    assert result.exit_code == 0
    result = runner.invoke(app, ["delete", file.name])
    assert result.exit_code == 0
    server_nodes = get_nodes(print=False)
    node_set = {(str(n.spec.name), str(n.spec.namespace)) for n in server_nodes}
    assert (node_dict["spec"]["name"], node_dict["spec"]["namespace"]) not in node_set
