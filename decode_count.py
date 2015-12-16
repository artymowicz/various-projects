"""Consider the code where the i'th letter of the alphabet is assigned the code word which is
the number i written in base 10. For example, a is assigned the code word 1 and letter z is
assigned the code word 26.
A message is encoded by concatenating the code words of each of its letters. For example,
abean would be encoded by the string of digits 125114. Note that lean would also be encoded
by the same string."""

fib = [1,2]

def decode_count(s):
	total = 1
	block_length = 0
	for i in range(len(s)):
		block_length += 1
		#print int(s[i:i+2])
		if int(s[i:i+2]) > 26:
			total = total*fibonacci(block_length)
			block_length = 0
	return total*fibonacci(block_length)

def fibonacci(n):
	if n == 1:
		return 1
	elif n == 2:
		return 2
	else:
		return fibonacci(n-2) + fibonacci(n-1)

print decode_count('125114')
