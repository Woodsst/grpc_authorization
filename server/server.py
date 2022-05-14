import logging
from concurrent import futures

import grpc

from server.authorization import Authorization
from server.config import Settings
from server.id_generator import token_generator
from server.orm import Orm
from server.registration import Registration
from server.server_pb2 import RegisterReply, RegisterCodeResult, LoginReply, LoginCodeResult
from server.server_pb2_grpc import GreeterServicer, add_GreeterServicer_to_server
from server.authorization import ClientStatus

logger = logging.getLogger()


class Server(GreeterServicer):

    def __init__(self):
        self.config = Settings()
        self.orm = Orm(self.config)

    def Login(self, request, context) -> LoginReply:
        auth = Authorization(request.user_name, request.user_passwd, self.orm)
        check = auth.client_authorization()
        if check == ClientStatus.CLIENT_AUTHORIZATION:
            token = token_generator(request.user_name)
            return LoginReply(code=LoginCodeResult.Value("LCR_ok"), token=token)
        return LoginReply(code=LoginCodeResult.Value("LCR_unknown_user"))

    def Register(self, request, context) -> RegisterReply:
        if len(request.user_name) <= 0 or len(request.user_passwd) <= 0:
            logger.info('%s - bad name or pass', request.user_name)
            return RegisterReply(code=RegisterCodeResult.Value('RCR_undefined'))

        logger.info('%s - register request', request.user_name)
        register = Registration(request.user_name, request.user_passwd, self.orm)
        if register.registration():
            token = token_generator(request.user_name)
            return RegisterReply(code=RegisterCodeResult.Value('RCR_ok'), reason=token)

        logger.info('%s - client exist', request.user_name)
        return RegisterReply(code=RegisterCodeResult.Value('RCR_already_exist'))

    def Connect(self, request_iterator, context):
        pass


def server_run():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_GreeterServicer_to_server(Server(), server)
    server.add_insecure_port('localhost:5000')
    server.start()
    server.wait_for_termination()
