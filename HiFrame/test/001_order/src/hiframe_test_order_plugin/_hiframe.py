def after_abc_aaa():
    pass

def after_abc_bbb():
    pass

def after_abc_ccc():
    pass

after_abc_aaa.key_list=[{"id":"after_abc"}]
after_abc_bbb.key_list=[{"id":"after_abc","after":[after_abc_aaa]}]
after_abc_ccc.key_list=[{"id":"after_abc","after":[after_abc_bbb]}]

###################

def after_cba_aaa():
    pass

def after_cba_bbb():
    pass

def after_cba_ccc():
    pass

after_cba_aaa.key_list=[{"id":"after_cba","after":[after_cba_bbb]}]
after_cba_bbb.key_list=[{"id":"after_cba","after":[after_cba_ccc]}]
after_cba_ccc.key_list=[{"id":"after_cba"}]

###################

def after2_aaa():
    pass

def after2_bbb():
    pass

def after2_ccc():
    pass

after2_aaa.key_list=[{"id":"after2"}]
after2_bbb.key_list=[{"id":"after2","after":[after2_aaa,after2_ccc]}]
after2_ccc.key_list=[{"id":"after2"}]

###################

def before_abc_aaa():
    pass

def before_abc_bbb():
    pass

def before_abc_ccc():
    pass

before_abc_aaa.key_list=[{"id":"before_abc","before":[before_abc_bbb]}]
before_abc_bbb.key_list=[{"id":"before_abc","before":[before_abc_ccc]}]
before_abc_ccc.key_list=[{"id":"before_abc"}]

###################

def before_cba_aaa():
    pass

def before_cba_bbb():
    pass

def before_cba_ccc():
    pass

before_cba_aaa.key_list=[{"id":"before_cba"}]
before_cba_bbb.key_list=[{"id":"before_cba","before":[before_cba_aaa]}]
before_cba_ccc.key_list=[{"id":"before_cba","before":[before_cba_bbb]}]

###################

def before2_aaa():
    pass

def before2_bbb():
    pass

def before2_ccc():
    pass

before2_aaa.key_list=[{"id":"before2"}]
before2_bbb.key_list=[{"id":"before2","before":[before2_aaa,before2_ccc]}]
before2_ccc.key_list=[{"id":"before2"}]

###################

def afterbefore_abc_aaa():
    pass

def afterbefore_abc_bbb():
    pass

def afterbefore_abc_ccc():
    pass

afterbefore_abc_aaa.key_list=[{"id":"afterbefore_abc"}]
afterbefore_abc_bbb.key_list=[{"id":"afterbefore_abc","after":[afterbefore_abc_aaa],"before":[afterbefore_abc_ccc]}]
afterbefore_abc_ccc.key_list=[{"id":"afterbefore_abc"}]

###################

def afterbefore_cba_aaa():
    pass

def afterbefore_cba_bbb():
    pass

def afterbefore_cba_ccc():
    pass

afterbefore_cba_aaa.key_list=[{"id":"afterbefore_cba"}]
afterbefore_cba_bbb.key_list=[{"id":"afterbefore_cba","after":[afterbefore_cba_ccc],"before":[afterbefore_cba_aaa]}]
afterbefore_cba_ccc.key_list=[{"id":"afterbefore_cba"}]
