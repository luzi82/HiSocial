import hipubiface

def helloworld():
    return hipubiface.ok(value="helloworld")
helloworld.key_list=[{"id":"HiPubIface.cmd"}]

def uppercase(txt_a):
    return hipubiface.ok(value=txt_a.upper())
uppercase.key_list=[{"id":"HiPubIface.cmd"}]

def hello_exception(txtf_upper):
    return hipubiface.ok(value=txtf_upper)
hello_exception.key_list=[{"id":"HiPubIface.cmd"}]
