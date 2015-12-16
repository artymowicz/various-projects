'''
A basic implementation of Eratosthenes' sieve, used to calculate the fist million primes.
At one point I was playing around with trying to optimize it but that's still half baked.
'''

import timeit
import math

N = 10**6

def sieve(n):
	a = [1]*(n)
	a[0] = 0#
	for i in range(2, int(math.sqrt(n))+1):
		if a[i]:
			for j in range(2*i, n, i):
				a[j] = 0
	return a

def fastSieve(n):
	a = [1]*(n/2)
	a[0] = 0

	for i in range(1,int(math.sqrt(n)/2+1)):
		#print i
		if a[i]:
			for j in xrange(3*i +1, n/2, 2*i+1):
				#print 'removing ' + str(2*j+1)
				a[j] = 0

			# j = 3*i + 1
			# increment = 2*i + 1
			# for i in xrange((n/2)/(2*i+1)-1):
			# 	a[j] = 0
			# 	j += increment
	return a

#testing
a = sieve(N)
o1 = ''
for i in range(2,N):
	if a[i]:
		o1 = o1 +  str(i) + ' '

b = fastSieve(N)
o2 = '2 '
for i in range(N/2):
	if b[i]:
		o2 = o2 +  str(2*i + 1) + ' '

#check whether or not the two algorithms agree
print o1==o2

#compare speeds
print 'slow sieve: ' + str(timeit.timeit(setup='from __main__ import sieve', stmt='sieve(10**6)', number=10)) + ' seconds'
print 'fast sieve: ' + str(timeit.timeit(setup='from __main__ import fastSieve', stmt='fastSieve(10**6)', number=10)) + ' seconds'