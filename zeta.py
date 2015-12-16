import math
import cmath
import matplotlib.pyplot as plt

#Computing some values of the zeta function

epsilon = 10e-15
max_iter = 10e6
r = 100
rang = 18.9

def zeta(s):
	z = 0
	n = 1
	a = 1
	while a > epsilon and n < max_iter:
		a = n**(-s)
		z += a
		n += 1
	return z, n

x = [1.1+rang*float(n)/r for n in range(r)]

y = []
z = (0,0)
for s in x:
	z = zeta(s)
	y.append(z[0])
	print s, z[1]
print

#plotting
plt.plot(x, y)
plt.yscale('linear')
plt.xlabel('$n$')
plt.ylabel('$\zeta(n)$')
plt.title('Naive approximation of $\zeta(n)$')
plt.axis([1, max(x), 0, max(y)])
plt.annotate(xy = (max(x)*0.7,max(y)*0.9),s ='$\epsilon=10^{-15},\ N=10^6$')
plt.show()