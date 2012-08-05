import hiframe

class T(hiframe.Plugin):

    def __init__(self,hf):
        hiframe.Plugin.__init__(self, hf)
        self.BUILD_COUNT = 0
        self.CLEAN_COUNT = 0
        self.START_COUNT = 0
        self.STOP_COUNT = 0
    
    def build(self):
        self.BUILD_COUNT = self.BUILD_COUNT+1
    build.key_list=[{"id":"HiFrame.build"}]
    
    def clean(self):
        self.CLEAN_COUNT = self.CLEAN_COUNT+1
    clean.key_list=[{"id":"HiFrame.clean"}]
    
    def start(self):
        self.START_COUNT = self.START_COUNT+1
    start.key_list=[{"id":"HiFrame.start"}]
    
    def stop(self):
        self.STOP_COUNT = self.STOP_COUNT+1
    stop.key_list=[{"id":"HiFrame.stop"}]
