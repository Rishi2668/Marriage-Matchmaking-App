from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy import types
from sqlalchemy.ext.declarative import declarative_base
import json
from database import Base

# Custom type to store lists in SQLite
class JsonList(types.TypeDecorator):
    impl = Text
    
    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)
        return value
    
    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    city = Column(String, index=True, nullable=False)
    interests = Column(JsonList, nullable=False, default=[])