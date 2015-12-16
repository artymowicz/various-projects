'''
Given a string that contains the numbers 1...n concatenated together, determine the index of n
in the string.

for example, index_in_range(12) would return 13 because the string '12' starts at the 13th index of the string "123456789101112"
'''

import math

def  index_in_range(x):
	i = 0
	j = 0
	while j < x:
		j += 1
		i += int(math.log(j))	
	return i-1

print index_in_range(15)