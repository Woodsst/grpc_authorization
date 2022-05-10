from client_data_for_tests import user, passwd
from server_pb2 import RegisterRequest, RegisterReply


def test_registration(server_start, send_message, orm):
    response = send_message.Register(
        RegisterRequest(
            user_name=user, user_passwd=passwd
        )
    )
    registration_token = orm.get_token()
    assert type(response) == RegisterReply
    assert response.code == 1
    assert response.reason == registration_token[0]


def test_registration_error(send_message, orm):
    response_bad_user = send_message.Register(
        RegisterRequest(
            user_name='', user_passwd=passwd
        )
    )
    assert type(response_bad_user) == RegisterReply
    assert response_bad_user.code == 0
    response_bad_passwd = send_message.Register(
        RegisterRequest(
            user_name=user, user_passwd=''
        )
    )
    assert type(response_bad_passwd) == RegisterReply
    assert response_bad_passwd.code == 0
    response = send_message.Register(
        RegisterRequest(
            user_name=user, user_passwd=passwd
        )
    )
    assert type(response) == RegisterReply
    assert response.code == 2
