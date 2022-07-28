import os
import time

import grpc
import pytest

from tests.config import Settings
from tests.orm import Orm
from tests.server_command import terminate_server
from server.proto_api.server_pb2_grpc import AuthorizationStub

config = Settings()


@pytest.fixture(scope='session')
def server_start():
    config.config_for_tests()
    os.popen('sh server_start.sh')
    time.sleep(1)
    yield
    config.reset_default_config()
    terminate_server()


@pytest.fixture(scope='function')
def orm():
    orm = Orm(config)
    yield orm
    orm.delete_test_client()


@pytest.fixture()
def send_message():
    with grpc.insecure_channel('localhost:5000') as channel:
        stub = AuthorizationStub(channel)
        yield stub
