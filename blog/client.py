import grpc

import blog_pb2
import blog_pb2_grpc
from bson.objectid import ObjectId

class BlogClient(object):
    """
    Client for gRPC Blog API
    """

    def __init__(self):
        self.host = "localhost"
        self.port = 50051

        # instantiate channel
        self.channel = grpc.insecure_channel(f"{self.host}:{self.port}")

        # bind with server
        self.client = blog_pb2_grpc.BlogServiceStub(self.channel)


    def get_blogs_list(self):

        # blog = blog_pb2.Blog(id=id)

        return self.client.ListBlogs()


if __name__ == "__main__":
    client = BlogClient()
    result = client.get_blogs_list()
    print(result)