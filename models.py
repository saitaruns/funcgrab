from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Function(Base):
    __tablename__ = "functions"

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String, index=True)
    function_name = Column(String, index=True)
    class_name = Column(String, index=True)
    repository_url = Column(String, index=True)
    code = Column(Text)
