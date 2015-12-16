
#Tried to make perfectprimes.py run faster:

import math
import timeit

N = 100

def sieve(n):
	a = [1]*(n)
	a[0] = 0#
	for i in xrange(2, int(math.sqrt(n))+1):
		if a[i]:
			for j in xrange(2*i, n, i):
				a[j] = 0
	a[1] = 0
	return a

#recursive algorithm to find all perfect primes of length n
def findpprimes(n, pcheck):
	if n==1:
		return [2,3,5,7]
	else:
		prev = findpprimes(n-1,pcheck)
		#print prev
		pprimes = []
		for p in prev:
			#append an odd digit other than 5 to the end of the number and check if the result is prime
			for k in [1,3,7,9]:
				t = 10*p + k
				if pcheck(t):
					pprimes.append(t)
		#print pprimes
		return pprimes

def pprimeFinder(N):

	primes = sieve(int(math.sqrt(10**N))+1) 

	def primecheck(n):
 		prime = True
		i = 0
		p = 2
		for i in xrange(2,int(math.sqrt(n)) + 1):
			if primes[i]:
				if n%i == 0:
					prime = False
					break
		return prime

	#print primecheck

	return findpprimes(N, primecheck)

print pprimeFinder(7)

#print timeit.timeit(setup='from __main__ import sieve', stmt='sieve(1001)', number=10)
print timeit.timeit(setup='from __main__ import pprimeFinder', stmt='pprimeFinder(6)', number=N)

