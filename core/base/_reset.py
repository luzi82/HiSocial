from base.Runtime import trace, trace_up, trace_down
from base import Database
from base.DatabaseBase import DBB
import os

def clean_order():
    return 0

def clean():
    trace_up("Clean database")
    db = Database.connect_mysqldb()
    db.query("SHOW TABLES")
    result = db.store_result()
    
    while True:
        row = result.fetch_row()
        if row == None:break
        if len(row)==0:break
        for i in row:
            table_name = i[0]
            trace("Remove table: "+table_name)
            db.query("DROP TABLE `"+table_name+"`")
    trace_down("done")
    db.commit()
    db.close()

def build_order():
    return 0

def build():
    trace_up("Build database")
    
    me=os.path.abspath(__file__)
    core_path=os.path.dirname(os.path.dirname(me))
    for i in os.listdir(core_path):
        if(os.path.isfile(core_path+"/"+i+"/_database.py")):
            trace("Module found: "+i)
            __import__(name=i,fromlist=["_database"])
            
    engine = Database.create_sqlalchemy_engine()
    DBB.metadata.create_all(engine)
    
    trace_down("done")
