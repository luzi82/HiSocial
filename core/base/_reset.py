from base.Runtime import trace, trace_up, trace_down
from base import Database

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
    pass
