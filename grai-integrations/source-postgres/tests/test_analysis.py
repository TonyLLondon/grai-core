from grai_client.endpoints.v1.client import ClientV1
from grai_source_postgres.base import update_server
from grai_source_postgres.loader import PostgresConnector

test_credentials = {
    "host": "localhost",
    "port": "5433",
    "dbname": "docker",
    "user": "docker",
    "password": "docker",
    "namespace": "test",
}


client = ClientV1("localhost", "8000")
client.set_authentication_headers("null@grai.io", "super_secret")


def test_update():
    update_server(client, **test_credentials)
