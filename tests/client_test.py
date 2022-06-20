from unittest.mock import MagicMock

from blog.client import BlogClient


class BlogClientTest(unittest.TestCase):


    def __init__(self):
        self.client = BlogClient()

    def read_test(self):
        read_blog = self.client.get('2')

