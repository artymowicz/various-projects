'''
CONIABILITY PROBLEM:
Given an array of integers and an integer N, return True iff N is a linear combination of elements of the array (with positive integer coefficients)
'''
array = [7,11,29,35,64]

N = 1000

#fast simple recursive algorithm
def coinable(n,a):
	if n < 1:
		return n == 0
	else:
		return any (coinable(n-x, a) for x in a)


#slow convoluted non-recursive solution
stack = []
def coinable2(n,a):
	stack = [n]
	
	while True:
		#print stack
		if stack == []:
			return False
		tmp = []
		for k in stack:
			tmp = tmp + [k-x for x in a]
		#print 'tmp = ' + str(tmp)
		stack = []
		for t in tmp:
			if t == 0:
				return True
			elif t > 0:
				stack.append(t)


print coinable(N,array)