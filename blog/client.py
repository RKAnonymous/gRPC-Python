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

    def get(self, id):
        blog = blog_pb2.Blog(id=id)
        return self.client.ReadBlog(blog)

    def list(self):
        return self.client.ListBlogs(blog_pb2.ListBlogRequest())

    def create(self, data):
        blog = blog_pb2.Blog(
            id=data["id"],
            author_id=data['author_id'],
            title=data['title'],
            content=data['content']
        )

        req = blog_pb2.CreateBlogReq(blog=blog)

        return self.client.CreateBlog(req)

    def update(self, id, data):
        print(
            data
        )
        data["id"] = id
        blog = blog_pb2.UpdateBlogReq(blog=data)
        return self.client.UpdateBlog(blog)

    def delete(self, id):
        request = blog_pb2.DeleteBlogReq(id=id)
        return self.client.DeleteBlog(request)



if __name__ == "__main__":
    client = BlogClient()
    request = [
        dict(
            id='2',
            author_id='32',
            title="title",
            content="content"
        ),
        dict(
            id='3',
            author_id='32',
            title="title",
            content="content"
        ),
        dict(
            id='1',
            author_id='32',
            title="title",
            content="content"
        )
    ]


    # LIST = client.list()
    # for l in LIST:
    #     print(l)
    # for r in request:
    #     CREATE = client.create(r)
    # GET = client.get('2')
    # print(GET)

    # UPDATE = client.update(id='2', data=d)
    # print(UPDATE)
    # DELETE = cli/