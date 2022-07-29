from concurrent import futures

import grpc

from server.authorization import Authorization
from server.id_generator import token_generator
from server.orm import Orm
from server.registration import Registration
from server.proto_api.server_pb2 import RegisterReply, RegisterCodeResult, LoginReply, LoginCodeResult
from server.proto_api.server_pb2_grpc import AuthorizationServicer, add_AuthorizationServicer_to_server
from server.authorization import ClientStatus
from server.logger_config import logger


class Server(AuthorizationServicer):

    def __init__(self, orm: Orm):
        self.orm = orm

    def Login(self, request, context) -> LoginReply:
        """Handler request for login"""

        auth = Authorization(request.user_name, request.user_passwd, self.orm)
        check = auth.client_authorization()
        if check == ClientStatus.CLIENT_AUTHORIZATION:
            token = token_generator(request.user_name, request.user_passwd)
            return LoginReply(code=LoginCodeResult.Value("LCR_ok"), token=token)
        return LoginReply(code=LoginCodeResult.Value("LCR_unknown_user"))

    def Register(self, request, context) -> RegisterReply:
        """Handler request for new username registration"""

        if not Registration.validation(request.user_name, request.user_passwd):
            logger.info('%s - bad name or pass', request.user_name)
            return RegisterReply(code=RegisterCodeResult.Value('RCR_undefined'))

        logger.info('%s - register request', request.user_name)
        register = Registration(request.user_name, request.user_passwd, self.orm)
        if register.registration():
            token = token_generator(request.user_name, request.user_passwd)
            return RegisterReply(code=RegisterCodeResult.Value('RCR_ok'), reason=token)

        logger.info('%s - client exist', request.user_name)
        return RegisterReply(code=RegisterCodeResult.Value('RCR_already_exist'))


def server_run(orm: Orm):
    """Start server run forever"""

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_AuthorizationServicer_to_server(Server(orm), server)
    server.add_insecure_port('localhost:5000')
    server.start()
    server.wait_for_termination()
