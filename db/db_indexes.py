from db.db_connection import collection


def blog_custom_index(field: str) -> None:
    collection.create_index(field)


def blog_id_index() -> None:
    collection.create_index('id')


def blog_author_id_index() -> None:
    collection.create_index('author_id')


if __name__ == "__main__":
    blog_author_id_index()
    blog_id_index()