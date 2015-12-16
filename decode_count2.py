def decode_count(s):
	total = 1
	k = 1
	k_prev = 1

	for i in range(len(s)-1):
		try:
			print i, s[i:i+2]
			if int(s[i:i+2]) > 26:
				total = total*k
				k = 1
				k_prev = 1
			else:
				(k, k_prev) = (k + k_prev, k)

		except TypeError:
			return 0
	return total*k

'''
print decode_count('1')
print decode_count('11')
print decode_count('111')
print decode_count('1111')
print decode_count('11111')
print decode_count('9999')
print decode_count('1119111')
print decode_count('01523')
'''

decode_count('1234')