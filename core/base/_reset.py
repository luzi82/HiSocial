from base.Runtime import trace, trace_up, trace_down
from base import Database

def clean_order():
    return 0

def clean():
    trace_up("Clean database")
    db = Database.connect_mysqldb()
    db.query("SHOW TABLES")
    table_list = db.store_result().fetch_row()
    for r in table_list :
        table_name=r[0]
        trace("Remove table: "+table_name)
        db.query("DROP TABLE "+table_name)
    trace_down("done")
    db.commit()
    db.close()

def build_order():
    return 0

def build():
    pass
