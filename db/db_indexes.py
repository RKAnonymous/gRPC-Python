from db.db_connection import collection
from pymongo import TEXT

def blog_custom_index(field: str) -> None:
    collection.create_index(field)


def blog_id_index() -> None:
    collection.create_index('id')


def blog_author_id_index() -> None:
    collection.create_index('author_id')

def blog_text_index() -> None:
    collection.create_index([("title", TEXT), ("content", TEXT)], name="search_index", default_language="english")


if __name__ == "__main__":
    blog_text_index()
    # blog_author_id_index()
    # blog_id_index()