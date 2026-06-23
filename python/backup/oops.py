
class Calculator:
    def __init__(self, a, b):
        self.number1 = a
        self.number2 = b

    def sum(self):
        return self.number1 + self.number2

    def sub(self):
        return self.number1 - self.number2

obj1 = Calculator(6, 7)
print (obj1)
obj2 = Calculator(10, 40)
print (obj2)
print ( obj1.sum() )
print ( obj2.sum() )

print (obj1.sub())

print (obj2.sub())



# var1 = 10
# print ("the result is", result)