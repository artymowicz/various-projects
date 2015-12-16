'''
PATTERN CHECK PROBLEM:
given lists or strings a1 and a2, determine whether a1 and a2 have the same 'pattern'. For example:


> patterncheck('aba', ['dog', 'cat', 'dog'])
True

> patterncheck(['dog', 'cat', 'dog'], 'aba')
True

> patterncheck([7,'asparagus',7], ['dog', 'cat', 'dog'])
True

> patterncheck('aab', ['dog', 'cat', 'dog'])
False

Just for fun, I decided to experimentally verify that the algorithm is indeed linear.
To this end, the algorithm is run N times with random input of length k with k ranging from 1 to K.
Average computation time is plotted against K to produce a satisfyingly linear-looking graph.

Note: for K = 1000, N = 10, the code takes ~30 seconds to run on my machine.
Included is an image of the output for K = 1000 with a large value of N (I don't remember exactly, something on the order of 500)

'''

K = 1000
N = 10

import timeit
import random
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter

#Solution:
def halfpatterncheck(a1,a2):
	same = True
	d = dict()
	for i in range(len(a1)):
		e = a1[i]
		if e in d:
			if not d[e] == a2[i]:
				same = False
				break
		else:
			d[e] = a2[i]
	return same

def patterncheck(a1,a2):
	return (halfpatterncheck(a1,a2) and halfpatterncheck(a2,a1))

##### Just for fun, verifying experimentally that runtime is linear #####

lengthRange = (1,K)

data = [0]*(lengthRange[1] - lengthRange[0])

for i in range(lengthRange[0], lengthRange[1]):
	for k in range(N):
		a = [random.randint(0,10) for x in range(i)]
		b = [random.randint(0,10) for x in range(i)]
		data[i-lengthRange[0]] += (timeit.timeit(setup='from __main__ import patterncheck, a,b', stmt='patterncheck(a,b)', number = 1))

print data
#plotting

plt.plot([d/N for d in data])
plt.xlabel('length of string')
plt.ylabel('average computation time')
plt.show()
