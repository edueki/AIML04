
# Data Types exercises for beginners
# String, Integer, Float, Bool
# This file includes simple examples and small exercises you can run and extend.

# --- Simple examples (original content preserved and slightly expanded) ---
var1 = 1.0
var2 = 2.0

print(f"sum of {var1} and {var2} is: {var1 + var2}")
print("Sum of {} and {} is: {}".format(var1, var2, var1 + var2))

var3 = """that's is "good day" is """
var4 = "HELLO"

var5 = var4.islower()

print(var3)
print(type(var3))


# --- Beginner exercises ---

def exercise1_variables():
	"""Exercise 1: basic integer/float arithmetic and formatting.
	- Create two numbers, compute their sum and average
	- Print results using f-strings and .format()
	- Use assertions to check expected values
	"""
	a = 5
	b = 3
	sum_ab = a + b
	avg = (a + b) / 2  # average of two numbers

	print('\nExercise 1: Variables and arithmetic')
	print(f"a = {a}, b = {b}")
	print(f"sum = {sum_ab}")
	print("average of {} and {} is: {}".format(a, b, avg))

	# simple checks
	assert sum_ab == 8
	assert isinstance(avg, float)
	return True


def exercise2_strings():
	"""Exercise 2: string operations.
	- Check length, casing, substring, replace, and splitting
	"""
	s = "Hello, World!"
	print('\nExercise 2: Strings')
	print('original:', s)
	print('length:', len(s))
	print('upper :', s.upper())
	print('lower :', s.lower())
	print('is lower?:', s.islower())
	print('contains "World"?:', 'World' in s)
	print('replace World->Universe:', s.replace('World', 'Universe'))
	print('split by comma:', s.split(','))

	assert len(s) == 13
	assert s.upper() == 'HELLO, WORLD!'
	return True


def exercise3_booleans():
	"""Exercise 3: Boolean values and comparisons."""
	x = 10
	y = 3
	print('\nExercise 3: Booleans and comparisons')
	print(f"x = {x}, y = {y}")
	print('x > y ->', x > y)
	print('x == y ->', x == y)
	print('x % y == 1 ->', (x % y) == 1)
	print('combined (x > y and x % y == 1) ->', (x > y) and ((x % y) == 1))

	assert (x > y) is True
	assert (x == y) is False
	return True


def exercise4_type_conversion():
	"""Exercise 4: Type conversion between strings and numbers."""
	print('\nExercise 4: Type conversion')
	s_int = "42"
	s_float = "3.14"
	i = int(s_int)
	f = float(s_float)

	print(f"string '{s_int}' -> int {i}")
	print(f"string '{s_float}' -> float {f}")

	assert i == 42
	assert abs(f - 3.14) < 1e-9

	# show how invalid conversion raises an error (handled here)
	try:
		invalid = int('abc')
	except ValueError:
		print("Converting 'abc' to int raises ValueError as expected")

	return True


def run_all_exercises():
	"""Run all exercises and print a summary."""
	print('\nRunning all exercises...')
	ok = True
	ok &= exercise1_variables()
	ok &= exercise2_strings()
	ok &= exercise3_booleans()
	ok &= exercise4_type_conversion()

	if ok:
		print('\nAll exercises completed successfully!')
	else:
		print('\nSome exercises failed. Check assertions or outputs above.')


if __name__ == '__main__':
	run_all_exercises()

