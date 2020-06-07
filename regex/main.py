import re

def Exponent(s):
	nums = re.findall(r'(\w+?)(\d+)', s)[0]
	return "$"+nums[0]+"^"+"{"+nums[1]+"}$"

def Fraction(s):
	nums = s.split("/")
	return r"$\frac"+"{"+nums[0]+"}"+"{"+nums[1]+"}$"

def addLatexSyntax(s):
	return "$\\"+s+"$"

def specialWords(s):
	words = ['alpha','beta','gamma']
	for item in words:
		if item in s:
			s = s.replace(item, addLatexSyntax(item))
	return s

fh = open('data.txt','r+')
content = fh.read()


exponent = re.compile(r'[a-z]+\d+')
frac = re.compile(r'\s+(\S+/\S+)\s*')

l = exponent.findall(content)
for item in l:
	it = Exponent(item)
	content = content.replace(item,it)

l = frac.findall(content)
for item in l:
	it = Fraction(item)
	content = content.replace(item,it)

content = specialWords(content)

fh.close()
open('data.txt', 'w').close()
fh = open('data.txt','w')
fh.write(content)
fh.close()