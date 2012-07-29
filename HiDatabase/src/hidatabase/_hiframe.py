import hidatabase
import os

def build(frame):
    data_path=frame.get_data_path(hidatabase.PLUGIN_KEY)
    config=frame.get_config()
    db_file=data_path+"/"+config.get(hidatabase.PLUGIN_KEY,"db_file")
    hidatabase._sqlalchemy_url="sqlite+pysqlite:///"+db_file
    
    os.makedirs(data_path)
    
    engine = hidatabase.create_sqlalchemy_engine()
    hidatabase.DBB.metadata.create_all(engine)

build.key_list=[{"id":"HiFrame.build"}]
