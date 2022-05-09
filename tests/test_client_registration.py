from client_data_for_tests import user, passwd
from server.server_pb2 import RegisterRequest, RegisterReply


def test_registration(send_message, orm):
    response = send_message.Register(
        RegisterRequest(
            user_name=user, user_passwd=passwd
        )
    )
    registration_token = orm.get_token()
    assert response.code == 1
    assert response.reason == registration_token[0]


def test_registration_error():
    pass
