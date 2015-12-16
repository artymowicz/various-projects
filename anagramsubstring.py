#Determines whether any anagram of the first string appears as a substring of the second string

a = 'xya'
b = 'aaaxyxaxyaaa'

def checkPermutation(s1,s2):
	d1 = dict()
	d2 = dict()

	for c in s1:
		if c in d1:
			d1[c] += 1
		else:
			d1[c] = 1

	for c in s2:
		if c in d2:
			d2[c] += 1
		else:
			d2[c] = 1


	for c in iter(d1):
		try:
			if not d1[c] == d2[c]:
				return False
		except KeyError:
			return False
	return True

def anagramSubstring(s1,s2):

	substrings = []
	contigious = ''
	for i in range(len(s2)): 
		#print i
		if s2[i] in s1:
			contigious = contigious + s2[i]

		else:
			if not contigious == '':
				substrings.append(contigious)
				contigious = ''

	substrings.append(contigious)

	for s in substrings:
		if checkPermutation(s1,s):
			return True

	return False

print anagramSubstring(a,b)



