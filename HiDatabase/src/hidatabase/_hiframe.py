import hidatabase
import os
import hiframe

class HiDatabase(hiframe.Plugin):

    def build(self):
        data_path=self.hiframe.get_data_path(hidatabase.PLUGIN_KEY)
        config=self.hiframe.get_config()
        db_file=data_path+"/"+config.get(hidatabase.PLUGIN_KEY,"db_file")
        hidatabase._sqlalchemy_url="sqlite+pysqlite:///"+db_file
        
        os.makedirs(data_path)
        
        engine = hidatabase.create_sqlalchemy_engine()
        hidatabase.DBB.metadata.create_all(engine)

    build.key_list=[{"id":"HiFrame.build"}]
