'''
# 为什么python不支持尾递归优化
import sys
sys.setrecursionlimit(15000)

def reduce(callback, arr, initValue=None, index=None):
    if (index == None): index = 0
    if (index >= len(arr)): return initValue
    if initValue == None:
        return reduce(callback, arr, arr[index], index+1)
    else:
        return reduce(callback, arr, callback(initValue, arr[index], index), index+1)
def reduceRight(callback, arr, initValue=None, index=None):
    if (index == None): index = len(arr)-1
    if (index < 0): return initValue
    if initValue == None:
        return reduceRight(callback, arr, arr[index], index-1)
    else:
        return reduceRight(callback, arr, callback(initValue, arr[index], index), index-1)
'''

def reduce(callback, arr, initValue=None):
    index = 0
    
    # 如果 initValue 是 None，使用数组的第一个元素作为初始值，并从第二个元素开始
    if initValue is None:
        if len(arr) == 0:
            raise TypeError("reduce() of empty sequence with no initial value")
        initValue = arr[0]
        index = 1

    # 使用循环来遍历数组
    while index < len(arr):
        initValue = callback(initValue, arr[index], index)
        index += 1

    return initValue

def reduceRight(callback, arr, initValue=None):
    index = len(arr) - 1

    # 如果 initValue 是 None，使用数组的最后一个元素作为初始值，并从倒数第二个元素开始
    if initValue is None:
        if len(arr) == 0:
            raise TypeError("reduceRight() of empty sequence with no initial value")
        initValue = arr[index]
        index -= 1

    # 使用循环来从右向左遍历数组
    while index >= 0:
        initValue = callback(initValue, arr[index], index)
        index -= 1

    return initValue

# 将不需要index的函数适配于reduce函数
def reduceAdaptor(func):
    return lambda pre, curr, index : func(pre, curr)

def map(callback, arr):
    def do(pre, curr, index):
        pre.append(callback(curr))
        return pre
    return reduce(do, arr, [])

def filter(callback, arr):
    def do(pre, curr, index):
        if(not callback(curr)):
            pre.append(curr)
        return pre
    return reduce(do, arr, [])

def pipe(*funcs):
    return lambda input: reduce(lambda pre, cur, index: cur(pre), *funcs, input)

def compose(*funcs):
    return lambda input: reduceRight(lambda pre, cur, index: cur(pre), *funcs, input)

# 柯里化，一个n参函数 -> n个单参函数
def curry(func, ignorableArgs=0, args=None):
    if (args == None): args = []
    def ret(input):
        args.append(input)
        if len(args) < func.__code__.co_argcount-ignorableArgs:
            return curry(func, ignorableArgs, args)
        else:
            return func(*args)
    return ret

def sort(callback, arr: list):
    return sorted(arr, key=callback)

# can't use the initValue
# To use the initValue, try lambda:
#   lambda initValue: fl.reduce(func, arr, initValue)
curried_reduce = lambda func: curry(reduce, 1)(func)
curried_reduceRight = lambda func: curry(reduceRight, 1)(func)
curried_map = lambda func: curry(map)(func)
curried_filter = lambda func: curry(filter)(func)
curried_sort = lambda func: curry(sort)(func)