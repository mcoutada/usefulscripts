def printobj1(my_object):
    for attribute in dir(my_object):
        if not attribute.startswith("__"):
            print(attribute)
            try:
                print(getattr(my_object, attribute)())
            except TypeError:
                print(getattr(my_object, attribute))
            
from pprint import pprint
def printobj2(my_object):
    pprint(vars(your_object))


from ppretty import ppretty

def printobj2(my_object):
    print ppretty(my_object, show_protected=True, show_static=True, show_properties=True)



class A(object):
    s = 5

    def __init__(self):
        self._p = 8

    @property
    def foo(self):
        return range(10)


printobj1(A())
printobj2(A())
printobj3(A())
