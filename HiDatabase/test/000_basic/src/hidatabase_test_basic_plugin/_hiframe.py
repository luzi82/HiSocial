from hidatabase import DBB
from sqlalchemy import Column, String, Integer

class TestTable(DBB):
    
    __tablename__ = "hidatabase_test_table"
    
    rid = Column(Integer, primary_key=True)
    data = Column(String(10))

    def __init__(self, rid, data):
        self.rid=rid
        self.data=data
