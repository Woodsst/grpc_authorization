import logging
from concurrent import futures

import grpc

from server.authorization import Authorization
from server.config import Settings
from server.id_generator import token_generator
from server.orm import Orm
from server.registration import Registration
from server.server_pb2 import RegisterReply, RegisterCodeResult
from server.server_pb2_grpc import GreeterServicer, add_GreeterServicer_to_server

logger = logging.getLogger()


class Server(GreeterServicer):

    def __init__(self):
        self.config = Settings()
        self.orm = Orm(self.config)

    def Login(self, request, context):
        auth = Authorization(request.user_name, request.user_passwd)
        auth.client_authorization()

    def Register(self, request, context) -> RegisterReply:
        if len(request.user_name) <= 0 or len(request.user_passwd) <= 0:
            logger.debug('%s - bad name or pass', request.user_name)
            return RegisterReply(code=RegisterCodeResult.Name(0))

        logger.info('%s - register request', request.user_name)
        register = Registration(request.user_name, request.user_passwd, self.orm)
        if register.registration():
            token = token_generator()
            self.orm.add_client_id(request.user_name, token)
            return RegisterReply(code=RegisterCodeResult.Name(1), reason=token)

        logger.debug('%s - client exist', request.user_name)
        return RegisterReply(code=RegisterCodeResult.Name(2))

    def Connect(self, request_iterator, context):
        pass


def server_run():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_GreeterServicer_to_server(Server(), server)
    server.add_insecure_port('localhost:5000')
    server.start()
    server.wait_for_termination()
