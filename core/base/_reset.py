from base import Database
from base.DatabaseBase import DBB
from base.Runtime import trace, trace_up, trace_down
import _mysql_exceptions
import os
import core_config
import shutil

def clean_order():
    return 0

def clean():
    trace_up("Clean database")
    db = Database.connect_mysqldb()
    dirty = True
    while dirty:
        dirty = False
        db.query("SHOW TABLES")
        result = db.store_result()
        while True:
            row = result.fetch_row()
            if row == None:break
            if len(row)==0:break
            dirty = True
            for i in row:
                table_name = i[0]
                trace("Remove table: "+table_name)
                try:
                    db.query("DROP TABLE `"+table_name+"`")
                except _mysql_exceptions.IntegrityError:
                    trace("fail, retry later")
    db.commit()
    db.close()
    trace_down("done")
    
    trace_up("Clean filesystem")
    data_folder=os.listdir(core_config.DATA_FOLDER)
    for i in data_folder:
        shutil.rmtree(core_config.DATA_FOLDER+"/"+i)
    trace_down("done")

def build_order():
    return 0

def build(install_config):
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
