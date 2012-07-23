BUILD_COUNT = 0
CLEAN_COUNT = 0
START_COUNT = 0
STOP_COUNT = 0

def build():
    global BUILD_COUNT
    BUILD_COUNT = BUILD_COUNT+1
build.key_list=[{"id":"HiFrame.build"}]

def clean():
    global CLEAN_COUNT
    CLEAN_COUNT = CLEAN_COUNT+1
clean.key_list=[{"id":"HiFrame.clean"}]

def start():
    global START_COUNT
    START_COUNT = START_COUNT+1
start.key_list=[{"id":"HiFrame.start"}]

def stop():
    global STOP_COUNT
    STOP_COUNT = STOP_COUNT+1
stop.key_list=[{"id":"HiFrame.stop"}]
