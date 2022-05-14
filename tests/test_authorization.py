from client_data_for_tests import USER, PASSWD, TOKEN
from server_pb2 import LoginRequest, RegisterRequest, LoginReply


def test_authorization(server_start, send_message, orm):
    send_message.Register(RegisterRequest(
        user_name=USER, user_passwd=PASSWD))
    response = send_message.Login(LoginRequest(
        user_name=USER, user_passwd=PASSWD))
    assert isinstance(response, LoginReply)
    assert response.code == 1
    assert response.token == TOKEN.decode()


def test_authorization_error(send_message, orm):
    response = send_message.Login(LoginRequest(
        user_name=USER, user_passwd=PASSWD))
    assert isinstance(response, LoginReply)
    assert response.code == 2
    send_message.Register(RegisterRequest(
        user_name=USER, user_passwd=PASSWD))
    response_bad_PASSWD = send_message.Login(LoginRequest(
        user_name=USER, user_passwd=''))
    assert isinstance(response_bad_PASSWD, LoginReply)
    assert response_bad_PASSWD.code == 2
