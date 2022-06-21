import time
import logging
import grpc

from typing import Generator
from google.protobuf.json_format import MessageToDict
from concurrent import futures
from db.db_connection import collection
from blog import blog_pb2_grpc
from blog.blog_pb2 import (
    Blog,
    ListBlogResponse,
    CreateBlogRes,
    UpdateBlogRes,
    DeleteBlogRes,
    SearchResponse,
    ReadBlogRes,
    ReadBlogReq,
    ListBlogRequest,
    CreateBlogReq,
    DeleteBlogReq,
    UpdateBlogReq,
    SearchRequest,
    GetByIDRequest,
    GetByIDResponse,
    GetByAuthorIDResponse,
    GetByAuthorIDRequest
)


_ONE_DAY_IN_SECONDS = 60*60*24


class BlogServiceCRUD(blog_pb2_grpc.BlogServiceServicer):

    def ListBlogs(self, request: ListBlogRequest, context) -> Generator[ListBlogResponse, None, None]:
        result = collection.find()
        for data in result:
            if data is not None:
                list_data = ListBlogResponse(
                    blog=Blog(
                        id=str(data["_id"]),
                        author_id=data['author_id'],
                        title=data['title'],
                        content=data['content']
                    )
                )
                yield list_data


    def ReadBlog(self, request: ReadBlogReq, context) -> ReadBlogRes:
        id: str = request.id
        data: dict = collection.find_one({"_id": id})

        response = Blog(
            id=data["_id"],
            author_id=data['author_id'],
            title=data['title'],
            content=data['content']
        )
        return ReadBlogRes(blog=response)


    def CreateBlog(self, request: CreateBlogReq, context) -> CreateBlogRes:
        data_create: dict = MessageToDict(request)["blog"]
        collection.insert_one({
            "_id": data_create["id"],
            "title": data_create["title"],
            "author_id": data_create["authorId"],
            "content": data_create["content"]
        })
        return CreateBlogRes(blog=request)


    def UpdateBlog(self, request: UpdateBlogReq, context) -> UpdateBlogRes:
        data_update: dict = MessageToDict(request)["blog"]
        id: str = data_update.pop("id")
        collection.replace_one(
            {
                "_id": id
            },
            {
                "author_id": data_update["authorId"],
                "title": data_update["title"],
                "content": data_update["content"]
            }
        )
        return UpdateBlogRes(success=True, msg=f"Blog with ID={id} is updated.")


    def DeleteBlog(self, request: DeleteBlogReq, context) -> DeleteBlogRes:
        id: str = MessageToDict(request)["id"]
        collection.delete_one({"_id": id})
        return DeleteBlogRes(success=True, msg=f"Blog with ID={id} is deleted.")


    def SearchBlog(self, request: SearchRequest, context) -> SearchResponse:
        query = request.query

        result = collection.find(
            {
                "$text": {
                    "$search": str(query)
                }
            }
        )
        for data in result:
            if data is not None:
                message = Blog(
                    id=data["_id"],
                    author_id=data["author_id"],
                    title=data['title'],
                    content=data['content']
                )
                yield SearchResponse(blog=message)

    def GetByID(self, request: GetByIDRequest, context) -> GetByIDResponse:
        id = request.id
        data = collection.find_one({"_id": id})
        message = Blog(
            id=data["_id"],
            author_id=data["author_id"],
            title=data['title'],
            content=data['content']
        )

        return GetByIDResponse(blog=message)

    def GetByAuthorID(self, request: GetByAuthorIDRequest, context) -> GetByAuthorIDResponse:
        id = request.author_id
        data = collection.find_one({"author_id": id})
        message = Blog(
            id=data["_id"],
            author_id=data["author_id"],
            title=data['title'],
            content=data['content']
        )

        return GetByAuthorIDResponse(blog=message)


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
