#determines the order of the automorphism taking z to z^k in the automorphism group of prime order p.
p = 43 
k = 1
a = [1]

while True:
	x = (a[-1]*k)%p
	if x == 1: break
	else: a.append(x)

print len(a)