numbers = [10, 50, 100, 150]
name = "prreddy"

def mystrfun(a):
    return a.upper()

def mynumfun(a):
    numbers.append(a)
    return numbers

mystrfun(name)
mynumfun(numbers)

print (name)
print (numbers)