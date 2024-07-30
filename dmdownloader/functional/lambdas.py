
def run_function(*args, **kwargs):
    """ When you have a function list and only want to call them, don't important the return, use this """
    def callback(func):
        func(*args, **kwargs)
    return callback

