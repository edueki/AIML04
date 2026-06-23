# def calc(**kwargs):
#     for key, value in kwargs.items():
#         print(key, value)
#
# calc(num1=20,num2=10,num3=50, num4=100)

# def cal2(a, *kwargs, **abc):
#     print (a)
#     for i in kwargs:
#         print(i)
#
# cal2(20, 50, 100, 150, 300, num1=10, num2=50, )

numbers = [10, 50, 100, 150]
name = "prreddy"

def mystrfun():
    return name.upper()

def mynumfun(a):
    numbers.append(a)
    return numbers
mystrfun()
mynumfun("5")

print (name)
print (numbers)





