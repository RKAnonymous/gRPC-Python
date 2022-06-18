import grpc

import blog_pb2
import blog_pb2_grpc


def run():
    with grpc.insecure_channel('localhost:50001') as channel:
        stub = blog_pb2_grpc.BlogServiceStub(channel)
        response = stub.B