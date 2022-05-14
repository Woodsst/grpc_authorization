from client_data_for_tests import USER, PASSWD, TOKEN
from server_pb2 import RegisterRequest, RegisterReply


def test_registration(send_message, orm):
    response = send_message.Register(
        RegisterRequest(
            user_name=USER, user_passwd=PASSWD
        ))
    assert isinstance(response, RegisterReply)
    assert response.code == 1
    assert response.reason == TOKEN.decode()


def test_registration_error(send_message, orm):
    send_message.Register(
        RegisterRequest(user_name=USER, user_passwd=PASSWD))
    response_bad_user = send_message.Register(
        RegisterRequest(
            user_name='', user_passwd=PASSWD
        ))
    assert isinstance(response_bad_user, RegisterReply)
    assert response_bad_user.code == 0
    response_bad_passwd = send_message.Register(
        RegisterRequest(
            user_name=USER, user_passwd=''
        ))
    assert isinstance(response_bad_passwd, RegisterReply)
    assert response_bad_passwd.code == 0
    response = send_message.Register(
        RegisterRequest(
            user_name=USER, user_passwd=PASSWD
        ))
    assert isinstance(response, RegisterReply)
    assert response.code == 2
