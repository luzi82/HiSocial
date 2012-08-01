import hipubiface

def command_helloworld():
    return hipubiface.ok(value="helloworld")
command_helloworld.key_list=[{"id":"HiPubIface.cmd.helloworld"}]

def command_uppercase(txt_a):
    return hipubiface.ok(value=txt_a.upper())
command_uppercase.key_list=[{"id":"HiPubIface.cmd.uppercase"}]

def command_uppercase_arg(txtf_upper):
    return hipubiface.ok(value=txtf_upper)
command_uppercase_arg.key_list=[{"id":"HiPubIface.cmd.uppercase_arg"}]

def argfilter_upper(v):
    return hipubiface.ok(value=v.upper())
argfilter_upper.key_list=[{"id":"HiPubIface.arg.upper"}]
