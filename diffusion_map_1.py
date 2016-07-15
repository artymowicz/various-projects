'''
An implementation of Coifman & Lafon's diffusion maps algorithm, based on the following paper:

Coifman, Ronald R., and Stephane Lafon. "Diffusion maps." Applied and computational harmonic analysis 21.1 (2006): 5-30.

'''

import numpy as np
import scipy
import math
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt

epsilon = 1
alpha = 1
delta = 0.1
t = 10

#arranges N points in dim dimensions into a spiral which rotates m times
def generateSpiral(N, dim, m):
	pts = np.zeros((N,dim))
	for i in range(N):
		pts[i] = [math.cos(m*2*math.pi*i/N)*(3+math.cos(2*math.pi*i/N))/4, 
		math.sin(m*2*math.pi*i/N)*(3+math.cos(2*math.pi*i/N))/4, (1 + math.sin(2*math.pi*i/N))/2] #MAAATH
	return pts

#generates N random numbers from 0 to 1
def generateRandom(N, dim):
	pts = np.zeros((N,dim))
	for i in range(N):
		pts[i] = [random.random(),random.random(),random.random()]
	return 0

#generates test data
def generatePoints(N, dim, noise = None , m = None, mode = 'spiral'):
	if mode == 'spiral':
		assert m != None
		return generateSpiral(N, dim, m)

	elif mode == 'rand':
		return generateRandom(N, dim)

	elif mode == 'noisySpiral':
		assert m != None
		assert noise != None
		return generateSpiral(N, dim, m) + noise*generateRandom(N, dim)

#plots points
def plot(pts, mode = 'scatter'):
	if len(pts.shape) == 1:
		pts = np.transpose([range(pts.shape[0]), pts])

	if pts.shape[1] == 3: #3D plotting
		fig = plt.figure()
		ax = fig.gca(projection='3d')
		ax.scatter(pts[:,0],pts[:,1], zs = pts[:,2])
		plt.show()

	elif pts.shape[1] == 2: #2D plotting
		if mode == 'scatter':
			plt.scatter(pts[:,0], pts[:,1])
			plt.show()
		elif mode == 'line':
			plt.plot(pts[:,0], pts[:,1])
			plt.show()
	else:
		print "data has incorrect dimensions"

def calculateKmatrix(pts, epsilon, alpha, kernel = 'exp'):
	N = pts.shape[0]
	a = np.zeros((N,N))
	if kernel == 'exp':
		for i in range(N):
			for j in range(N):
				a[i,j] = math.exp(-((pts[i][0] - pts[j][0])**2 + (pts[i][1] - pts[j][1])**2 + (pts[i][1] - pts[j][1])**2)/epsilon) #MAAAAAATH
	return a

def calculateDensities(kMatrix, epsilon):
	N = kMatrix.shape[0]
	q = np.zeros(N)
	for i in range(N):
		for j in range(N):
			q[i] += kMatrix[i][j]
	return q

def recalculateKmatrix(kMatrix, q):
	N = kMatrix.shape[0]
	kMatrix_alpha = np.zeros((N,N))
	for i in range(N):
		for j in range(N):
			kMatrix_alpha[i][j] = kMatrix[i][j]/(q[i]*q[j])
	return kMatrix_alpha

def calculateNormalizedDensity(kMatrix_alpha):
	N = kMatrix_alpha.shape[0]
	density = np.zeros(N)
	for i in range(N):
		for j in range(N):
			density[i] += kMatrix_alpha[i][j]
	return density

def calculateTransitionKernel(kMatrix_alpha, density):
	N = kMatrix_alpha.shape[0]
	pMatrix = np.zeros((N,N))
	for i in range(N):
		for j in range(N):
			pMatrix[i][j] = kMatrix_alpha[i][j]/density[i]
	return pMatrix

#checks if a matrix deviates too far from being symmetric (worst case) 
def checkSymmetric(matrix, eps):
	m = matrix - np.transpose(matrix)
	return np.max(m)<eps

#checks if a set of vectors deviates too much from being orthonormal (worst case)
def checkOrthonormal(vectors, eps):
	maximum = 0
	N = eig.shape[1]
	for i in range(N):
		for j in range(i,N):
			prod = np.dot(vectors[i], vectors[j])
			if i != j:
				maximum = max(maximum, abs(prod))
	return maximum < eps

#checks if a set of vectors deviates too much from being orthonormal (on average)
def checkOrthonormalAvg(vectors, eps):
	dotProducts = 0
	N = vectors.shape[1]

	for i in range(N):
		for j in range(i,N):
			prod = np.dot(vectors[i], np.conj(vectors[j]))
			if i != j:
				dotProducts += abs(prod)

	avgDot = dotProducts/((N*(N - 1))/2)
	return avgDot < eps

#computes s(delta, t)
def computeEmbedDim(spectrum, delta, t):
	s = len(spectrum)-1 #s = len(spectrum) doesn't work. In the embedding, the first eigenfunction must be ignored, so s has to be < dim
	l = 1
	while s == len(spectrum)-1 and l < len(spectrum)-1:
		if abs(spectrum[l]) < (delta**(1./t))*abs(spectrum[1]):
			s = l
		l += 1
	return s

#embeds a collection of points using eigenvalues of P
def embedPoints(pts, eigValues, eigVectors, s, t):
	embedPts = np.zeros((pts.shape[0], s))

	for i in range(pts.shape[0]):
		for j in range(s):
			embedPts[i][j] = (eigValues[j+1]**t)*eigVectors[j+1][i]

	return embedPts

points = generatePoints(300, 3, m = 2)
plot(points)
kMatrix = calculateKmatrix(points, epsilon, alpha)
q = calculateDensities(kMatrix, epsilon)
kMatrix_alpha = recalculateKmatrix(kMatrix, q)
density = calculateNormalizedDensity(kMatrix_alpha)
pMatrix = calculateTransitionKernel(kMatrix_alpha, density)

#making sure the diffusion matrix is sufficiently close to being symmetric (worst case)
assert checkSymmetric(pMatrix, 0.1)

#calculating the spectrum of pMatrix (we flip them because np.linalg.eigh orders eigenvalues small-large)
eigValues, eigVectors = np.linalg.eigh(pMatrix)
eigValues = np.flipud(eigValues)
eigVectors = np.transpose(np.fliplr(eigVectors))
 
#making sure the eigenbasis is sufficiently orthonormal (on average)
assert checkOrthonormalAvg(eigVectors, 0.1)

#plot(eigValues)
s = computeEmbedDim(eigValues, delta, t)

print "embedding dimension:", s

plot(embedPoints(points, eigValues, eigVectors, s, t), mode = 'line')

