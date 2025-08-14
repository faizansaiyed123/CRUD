from src.configs.config import engine
from functools import lru_cache
from sqlalchemy import Table, MetaData
from sqlalchemy.util import memoized_property

@lru_cache()
class Tables:
    def __init__(self):
        self.metadata = MetaData()
        self.metadata.bind = engine

    @memoized_property
    def users(self):
        return Table("users", self.metadata, autoload_with=engine)


    @memoized_property
    def posts(self):
        return Table("posts", self.metadata, autoload_with=engine)


    @memoized_property
    def likes(self):
        return Table("likes", self.metadata, autoload_with=engine)


    @memoized_property
    def comments(self):
        return Table("comments", self.metadata, autoload_with=engine)

