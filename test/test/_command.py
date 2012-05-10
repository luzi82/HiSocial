import base.Command
import os.path
import hashlib

def command_helloworld():
    return base.Command.ok(value="helloworld")

def command_uppercase(txt_a):
    return base.Command.ok(value=txt_a.upper())

def command_uppercase_arg(txtf_test_upper):
    return base.Command.ok(value=txtf_test_upper)

def command_file_md5sum(file_v):
    file_bin = file_v.read()
    file_v.close()
    h = hashlib.md5()
    h.update(file_bin)
    h = h.hexdigest()
    return base.Command.ok(value=h)

def argfilter_upper(v):
    return base.Command.ok(value=v.upper())

def file_hellofile():
    tmp=os.path.abspath(__file__) # ../test/test/_command.py
    tmp=os.path.dirname(os.path.dirname(tmp)) # ../test
    tmp=tmp+"/res/test0.torrent.txt" # ../test/res/test0.torrent.txt
    return base.Command.ok(result={
        "file_type":"local",
        "mime":"text/plain; charset=us-ascii",
        "file_name":tmp,
    })

def file_hellofile2():
    tmp=os.path.abspath(__file__) # ../test/test/_command.py
    tmp=os.path.dirname(os.path.dirname(tmp)) # ../test
    tmp=tmp+"/res/test0.torrent.txt" # ../test/res/test0.torrent.txt
    return base.Command.ok(result={
        "file_type":"local",
        "file_name":tmp,
    })

def file_helloimage():
    tmp=os.path.abspath(__file__) # ../test/test/_command.py
    tmp=os.path.dirname(os.path.dirname(tmp)) # ../test
    tmp=tmp+"/res/math0.png" # ../test/res/math0.png
    return base.Command.ok(result={
        "file_type":"local",
        "file_name":tmp,
    })
