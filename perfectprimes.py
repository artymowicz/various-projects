N = 3

#returns an array of 1s and 0s that tell you which numbers less than n are prime (basic sieve with a few minor optimizations)
def sieve(n):
	a = [1]*(n)
	a[0] = 0#
	for i in range(2,n/2):
		if a[i]:
			for j in range(2*i, n, i):
				a[j] = 0
	return a

#recursive algorithm to find all perfect primes of length n
def findpprimes(n, a):
	if n==1:
		return [2,3,5,7]
	else:
		prev = findpprimes(n-1, a)
		pprimes = []
		for p in prev:
			#append an odd digit other than 5 to the end of the number and check if the result is prime
			for k in [1,3,7,9]:
				t = 10*p + k
				if a[t] == 1:
					pprimes.append(t)
		return pprimes

#funcion calls
o = []
for p in findpprimes(N, sieve(10**N)):
	o.append(p)
print o