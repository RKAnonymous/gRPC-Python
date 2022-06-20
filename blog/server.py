import json
import time
import logging
import grpc
from bson.objectid import ObjectId
from concurrent import futures
from db.db_connection import client
from blog_pb2 import Blog, CreateBlogRes, UpdateBlogRes, ReadBlogRes, DeleteBlogRes, ListBlogResponse
import blog_pb2_grpc


_ONE_DAY_IN_SECONDS = 60*60*24


class BlogServiceCRUD(blog_pb2_grpc.BlogServiceServicer):

    def Connection(self):
        assert client.blog is not None, "BLOG Collection was not found!"
        return client.blog


    def ListBlogs(self):
        query = self.Connection()

        result = query.find({})

        for data in result:
            if data is not None:
                list_data = ListBlogResponse(
                    id=str(data["_id"]),
                    author_id=data['author_id'],
                    title=data['title'],
                    content=data['content']
                )
                yield list_data


    def ReadBlog(self, request, context):
        query = self.Connection()

        id = request.id
        data = query.find_one({"_id": ObjectId(id)})

        return ReadBlogRes(
            id=data["_id"],
            author_id=data['author_id'],
            title=data['title'],
            content=data['content']
        )


    def CreateBlog(self, request, context):
        query = self.Connection()

        data_insert = dict(
            author_id=request.author_id,
            title=request.title,
            content=request.content,
        )

        query.insert_one(data_insert)
        return CreateBlogRes(data_insert)


    def UpdateBlog(self, request, context):
        query = self.Connection()
        id = request.id
        data_update = dict(
            author_id=request.author_id,
            title=request.title,
            content=request.content,
        )

        query.replace_one({"_id": ObjectId(id)}, data_update)
        return UpdateBlogRes(success=True, msg=f"Blog with ID={id} is updated.")


    def DeleteBlog(self, request, context):
        query = self.Connection()
        id = request.id

        query.delete_one({"_id": ObjectId(id)})
        return DeleteBlogRes(success=True, msg=f"Blog with ID={id} is deleted.")


def run():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    blog_pb2_grpc.add_BlogServiceServicer_to_server(BlogServiceCRUD(), server)
    server.add_insecure_port('0.0.0.0:50051')
    server.start()
    server.wait_for_termination(timeout=15)

    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)



if __name__ == "__main__":
    print("Starting server...")
    logging.basicConfig()
    run()
