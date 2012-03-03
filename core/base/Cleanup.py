class Cleanup(object):

    cleanup_stack = []
    
    def __init__(self):
        pass
    
    def __del__(self):
        self.clean_all()
    
    def push(self, func):
        self.cleanup_stack.append(func)

    def clean(self):
        self.pop()()

    def pop(self):
        return self.cleanup_stack.pop()

    def clean_all(self):
        while len(self.cleanup_stack) > 0:
            self.clean()
