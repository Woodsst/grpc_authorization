import grpc
import pytest
from server.server_pb2_grpc import GreeterStub
from orm import Orm
from config import Settings

config = Settings()


@pytest.fixture()
def server_status():
    pass


@pytest.fixture()
def orm():
    orm = Orm(config)
    yield orm


@pytest.fixture()
def send_message():
    with grpc.insecure_channel('localhost:5000') as channel:
        stub = GreeterStub(channel)
        yield stub
