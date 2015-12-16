#Playing around with the Legendre symbol

import math

N = 10
M = 10

#returns the Legendre symbol (n/q)
def legendre(n,q):
	#r = (n**((q-1)/2))%q
	r = 1
	for i in range((q-1)/2):
		r = r*n%q
	return int(r - int(r > 1)*q)

#Simple sieve to find primes below N
prime = N*[True]
prime[0] = False
prime[1] = False
for i in range(2, int(math.sqrt(N))+1):
	if prime[i]:
		j = 2*i
		while j < N:
			prime[j] = False
			j += i

#making a list of primes below N
primes = []
for i in range(N):
	if prime[i]:
		primes.append(i)


#testing
print [legendre(n,7) for n in range(100)]
