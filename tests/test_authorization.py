from client_data_for_tests import user, passwd
from server_pb2 import LoginRequest, RegisterRequest, LoginReply


def test_authorization(server_start, send_message, orm):
    send_message.Register(RegisterRequest(
        user_name=user, user_passwd=passwd))
    response = send_message.Login(LoginRequest(
        user_name=user, user_passwd=passwd))
    authorization_token = orm.get_token()
    assert type(response) == LoginReply
    assert response.code == 1
    assert response.token == authorization_token[0]


def test_authorization_error(send_message, orm):
    response = send_message.Login(LoginRequest(
        user_name=user, user_passwd=passwd))
    assert type(response) == LoginReply
    assert response.code == 2
    send_message.Register(RegisterRequest(
        user_name=user, user_passwd=passwd))
    response_bad_passwd = send_message.Login(LoginRequest(
        user_name=user, user_passwd=''))
    assert type(response_bad_passwd) == LoginReply
    assert response_bad_passwd.code == 2
