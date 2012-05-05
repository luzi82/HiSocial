import base.Command

def command_helloworld():
    return base.Command.ok(value="helloworld")

def command_uppercase(txt_a):
    return base.Command.ok(value=txt_a.upper())

def command_uppercase_arg(txtf_test_upper):
    return base.Command.ok(value=txtf_test_upper)

def argfilter_upper(v):
    return base.Command.ok(value=v.upper())
