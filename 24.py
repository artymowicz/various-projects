
'''
THE 24 PROBLEM:
Given a list of 4 numbers, determine if they can be combined using the arithmetic operations + - x / (including brackets) to make the number 24

codegolf solution
'''
nums = [3,8,0,0]

import itertools, numpy

def combiner(a):
	return a if len(a) == 1 else sum([combiner([operation(a[pair[0]], a[pair[1]])] + list(a[i] for i in range(len(a)) if i not in pair)) for operation in [numpy.add, numpy.divide, numpy.multiply, numpy.subtract] for pair in itertools.permutations(range(len(a)),2)],[]) # LOL

print any(x == 24 for x in combiner(nums))