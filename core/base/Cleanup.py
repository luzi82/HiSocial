class Cleanup(object):
    """
    A cleanup stack to do auto cleanup in scope.
    """

    cleanup_stack = []
    
    def __init__(self):
        pass
    
    def __del__(self):
        self.clean_all()
    
    def push(self, func):
        """
        Add a function in cleanup stack.
        The function will be called when:
        - clean()
        - clean_all()
        - object deleted
        
        @type func: Function
        @param func: Function to be called for cleanup
        """
        self.cleanup_stack.append(func)

    def clean(self):
        """
        Pop a cleanup function from stack and call the function.
        """
        self.pop()()

    def pop(self):
        """
        Pop a cleanup function from stack without calling the function.
        
        @rtype: Function
        @return: The cleanup function have put to stack
        """
        return self.cleanup_stack.pop()

    def clean_all(self):
        """
        Pop all cleanup function and call all functions
        """
        while len(self.cleanup_stack) > 0:
            self.clean()
