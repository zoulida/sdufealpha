__author__ = 'zoulida'
from functools import reduce
def wrapper():
    alist=range(1,101)
    def lazy_sum():
        return reduce(lambda x,y:x+y,alist)
    return lazy_sum
pp = wrapper()
print (pp)
print (pp())
