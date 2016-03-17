'''
Modelling a simple spin 2D glass. Atoms are arranged on a square lattice. 
Up-up and down-down interaction energies are -1, and up-down interaction energy is +1.
Only nearest-neighbour interactions are considered, with equal weightings given to all neighbours.

Spins are allowed to flip between up and down, following a Boltzmann probablility law. 
To preserve a user-specified ratio of up spins to down spins, over-represented spin values are energetically penalized.
Annealing is achieved by an exponential decrease in temperature.

HOW TO USE:
Running lattice2.py creates a sequence of images in ./lattice/
To make a movie from these, go to ./lattice/ and run:

ffmpeg -framerate 200 -i lattice%05d.png -c:v libx264 -r 30 -pix_fmt yuv420p out.mp4

'''

import numpy as np
import matplotlib
matplotlib.use('TKAgg')
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import math
import random
import matplotlib.animation as animation
from scipy.misc import imsave
from scipy import signal

N = 200		#size of lattice
r = 0.5		#desired ratio of up to down
M = 5000	#number of iterations
B = 100		#batch size
a = 10 		#parameter for ratio regulation
T = 1000 		#temperature
prob_cutoff = 5 #when |g/T| exceeds this parameter, probablility is 1 or 0
temp_annealing_factor = 1 - 0.001*math.log(M)		#temperature is multiplied by this factor each iteration
ratio_annealing_factor = 1 + 0.0001*math.log(M)

def compute_excess(image):
	s = 0
	for i in range(image.shape[0]):
		for j in range(image.shape[1]):
			s += image[i][j]
	return s

def calculate_p(g,T):
	if g/T > prob_cutoff:
		return 0
	elif g/T < -prob_cutoff:
		return 1
	else:
		return math.exp(-g/T)/(math.exp(g/T) + math.exp(-g/T))

def choose_batch(N,B):
	batch = []
	i = 0
	while i < B:
		x = random.randint(0,N-1)
		y = random.randint(0,N-1)
		if not (x,y) in batch:
			batch.append((x,y))
			i += 1
	return batch

def update_lattice(old_lattice,new_lattice, g, T, s, (x,y)):
	p = calculate_p(g[x][y] - a*s/(N*N),T)
	#print "point: ", (x,y), "field strength:", g[x][y], "probability up:", p
	'''
	if rand[j][k] < p:
				lattice[i+1][j][k] = 1
				if lattice[i][j][k] == -1:
					s += 2
					g[x+1][y] += 
			else:
				lattice[i+1][j][k] = -1
				if lattice[i][j][k] == 1:
					s -= 2
	'''
	rand = random.random()
	new_lattice[x][y] = 1 - 2*(rand < p)
	difference = new_lattice[x][y] - old_lattice[x][y]
	#print "rand: ", rand, "new_lattice[x][y]:", new_lattice[x][y], "old_lattice[x][y]:", old_lattice[x][y]
	#print id(new_lattice), id(old_lattice)
	if difference != 0:
		for i in range(-1,1):
			for j in range(-1,1):
				g[x+i][y+j] += difference
				s += difference

	g[x][y] -= difference
	return s

#initializations
lattice = []
lattice.append(np.empty((N,N)))
lattice[0].fill(-1)

kernel = np.zeros((N,N))

#define interaction kernel
for i in range(-1,1):
	for j in range(-1,1):
		kernel[i][j] = 1
kernel[0][0] = 0

#randomly populate the lattice
for i in range(N):
	for j in range(N):
		if (random.random() < r):
			lattice[0][i][j] = 1;

#initialize g,s,p
g = -np.multiply(lattice[0], signal.convolve2d(lattice[0],kernel, mode = 'same', boundary = 'wrap')) #computing the field at each point
s = compute_excess(lattice[0]) #spin excess

#plotting
fig = plt.figure()

#main loop
for i in range(M):

	#make a new lattice frame
	lattice.append(np.copy(lattice[i]))

	#randomly picking a batch of size B
	batch = choose_batch(N,B)

	print 'iteration:',i,'spin excess:', s

	#all the work is done here
	for point in batch:
		s = update_lattice(lattice[i], lattice[i+1], g, T, s, point)

	#annealing
	T = T*temp_annealing_factor
	a = a*ratio_annealing_factor

#creating the video
for i in range(M+1):
	print 'writing image' + 'lattice' + str(i).zfill(5) + '.png'
	imsave('./lattice/lattice' + str(i).zfill(5) + '.png', lattice[i])



