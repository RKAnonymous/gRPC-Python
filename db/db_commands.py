import click
from client import client


# @click.command()
# @click.command("--name", default="mydb", help="Name of new database")
# @click.argument('name')
def create_db(name):
    mydb = client[f"{name}"]
    post_collection = mydb["posts"]
    assert mydb is not None, "Database was not created."
    print("Databse is created successfully.")



def get_database():
    return client["mydb"]

def create_table(table_name):
    db = get_database()
    table = db[f'{table_name}']




if __name__ == "__main__":
    create_db("mydb")
    get_database()