import os
import subprocess
import core_config
import TorrentStorage

def build_order():
    return 20

def build(install_config):
    me=os.path.abspath(__file__)
    me_path=os.path.dirname(me)
    p1 = subprocess.Popen([
                            "cat",
                            me_path+"/xbt_tracker.sql"
                           ],
                          stdout=subprocess.PIPE)
    p2 = subprocess.Popen([
                            "mysql",
                            "--host="+core_config.DB_SERVER,
                            "--user="+core_config.DB_USERNAME,
                            "--password="+core_config.DB_PASSWORD,
                            "--default-character-set=utf8",
                            core_config.DB_SCHEMATA
                           ],
                          stdin=p1.stdout,
                          stdout=subprocess.PIPE)
    p2.wait()

    os.makedirs(TorrentStorage.STORAGE_PATH)
    os.chmod(TorrentStorage.STORAGE_PATH,0777)
