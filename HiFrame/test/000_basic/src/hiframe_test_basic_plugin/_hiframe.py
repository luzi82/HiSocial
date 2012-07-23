def simple_func():
    return "simple ret"
simple_func.key_list=[{"id":"simple"}]

def simple_arg_func(abc):
    return abc+1
simple_arg_func.key_list=[{"id":"simple_arg"}]

def order_a():
    return "a"
order_a.key_list=[{"id":"order"}]

def order_b():
    return "b"
order_b.key_list=[{"id":"order","order":1}]

def order_c():
    return "c"
order_c.key_list=[{"id":"order","order":-1}]

def pkg2_a():
    return "a"
pkg2_a.key_list=[{"id":"pkg2","order":100}]

def pkg2_c():
    return "c"
pkg2_c.key_list=[{"id":"pkg2","order":0}]

def no_order_a():
    return "a"
no_order_a.key_list=[{"id":"no_order"}]

def no_order_b():
    return "b"
no_order_b.key_list=[{"id":"no_order"}]
