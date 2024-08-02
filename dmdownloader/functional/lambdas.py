""" Some useful callback """

run_function = lambda *args, **kwargs: lambda func: func(*args, **kwargs)
""" When you have a function list and only want to call them, don't important the return, use this """

