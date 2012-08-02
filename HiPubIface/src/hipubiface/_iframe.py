import hipubiface

def start(frame):
    hipubiface._func_list = frame.get_func_list("HiPubIface.cmd")
start.key_list=[{"id":"HiFrame.start"}]

def stop(frame):
    hipubiface._func_list = None
stop.key_list=[{"id":"HiFrame.stop"}]
