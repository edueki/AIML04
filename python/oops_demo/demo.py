# Calculator app - add, sub, mul etc...

# class Calculator:
    # Methods - add(), sub(), mul()

from cal.core import *

obj = Calculator()
result = obj()
print(result)

response = obj.add(1,2)
print ("sum is: ", response)