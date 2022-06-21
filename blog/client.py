import grpc
import blog_pb2
import blog_pb2_grpc

from typing import List
from google.protobuf.json_format import MessageToDict


class BlogClient(object):
    """
    Client for gRPC Blog API
    """

    def __init__(self):
        self.host: str = "localhost"
        self.port: int = 50051

        # instantiate channel
        self.channel = grpc.insecure_channel(f"{self.host}:{self.port}")

        # bind with server
        self.client = blog_pb2_grpc.BlogServiceStub(self.channel)

    def get(self, id: int) -> dict:
        blog_pb = blog_pb2.Blog(id=id)
        blog_data = self.client.ReadBlog(blog_pb)
        return MessageToDict(blog_data)

    def list(self) -> List[dict]:
        blog_list = self.client.ListBlogs(blog_pb2.ListBlogRequest())
        converted_to_dict = [MessageToDict(data) for data in blog_list]
        return converted_to_dict

    def create(self, data: dict) -> dict:
        blog = blog_pb2.Blog(
            id=data["id"],
            author_id=data['author_id'],
            title=data['title'],
            content=data['content']
        )

        blog_pb = blog_pb2.CreateBlogReq(blog=blog)
        created_blog = self.client.CreateBlog(blog_pb)

        return MessageToDict(created_blog)

    def update(self, id: str, data: dict) -> dict:
        data["id"] = id
        blog_pb = blog_pb2.UpdateBlogReq(blog=data)
        updated_blog = self.client.UpdateBlog(blog_pb)
        return MessageToDict(updated_blog)

    def delete(self, id: str) -> dict:
        blog_pb = blog_pb2.DeleteBlogReq(id=id)
        deleted_blog = self.client.DeleteBlog(blog_pb)
        return MessageToDict(deleted_blog)

    def search(self, query: str) -> List[dict]:
        blog_pb = blog_pb2.SearchRequest(query=query)
        search_blog = self.client.SearchBlog(blog_pb)
        converted_to_dict = [MessageToDict(data) for data in search_blog]
        return converted_to_dict

    def get_by_id(self, id: str):
        blog_pb = blog_pb2.GetByIDRequest(id=id)
        data = self.client.GetByID(blog_pb)
        return data

    def get_by_author_id(self, author_id):
        blog_pb = blog_pb2.GetByAuthorIDRequest(author_id=author_id)
        data = self.client.GetByAuthorID(blog_pb)
        return data



if __name__ == "__main__":
    client = BlogClient()