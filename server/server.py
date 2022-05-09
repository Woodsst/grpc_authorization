from concurrent import futures
from server.authorization import Authorization
from server.registration import Registration
from server.orm import Orm
from server.config import Settings
from server.id_generator import token_generator

import grpc
from server.server_pb2_grpc import GreeterServicer, add_GreeterServicer_to_server
from server.server_pb2 import RegisterReply, RegisterCodeResult


class Server(GreeterServicer):

    def __init__(self):
        self.config = Settings()
        self.orm = Orm(self.config)

    def Login(self, request, context):
        auth = Authorization(request.user_name, request.user_passwd)
        auth.client_authorization()

    def Register(self, request, context):
        register = Registration(request.user_name, request.user_passwd, self.orm)
        register.registration()
        token = token_generator()
        self.orm.add_client_id(request.user_name, token)
        if token:
            return RegisterReply(code=RegisterCodeResult.Name(1), reason=token)

    def Connect(self, request_iterator, context):
        pass


def server_run():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_GreeterServicer_to_server(Server(), server)
    server.add_insecure_port('localhost:5000')
    server.start()
    server.wait_for_termination()

