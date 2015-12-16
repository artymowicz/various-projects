'''
PALINDROME INDEX PROBLEM:
You are given a string of lowercase letters. Your task is to figure out the index of the character on whose removal will make the string a palindrome. 
There will always be a valid solution. 

In case string is already palindrome, then -1 is also a valid answer along with possible indices.
'''

string = 'abcdefggfedcba'

def palindromeIndex(s):
	k = -1
	for i in range(len(s)):
		if not s[i] == s[-(i+1)]:
			k = i
			break
			
	if k == -1:
		return -1
	else:
		tmp = s[:k] + s[k+1:]
		if tmp == tmp[::-1]:
			return k
		else:
			return len(s) - k - 1

print palindromeIndex(string)