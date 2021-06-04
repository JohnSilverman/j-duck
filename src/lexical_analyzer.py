def error(codestring, i):
	print("Unexpected token \"%s\" at ch %d"%(codestring[i:i+10],i))
	exit(0)

def isDigit(ch):
	return (ord(ch)>=ord('0') and ord(ch)<=ord('9'))

def isAlpha(ch):
	return (ord(ch) >= ord('a') and ord(ch) <= ord('z'))\
		or (ord(ch) >= ord('A') and ord(ch) <= ord('Z'))\
			or ch=='_'

#use this function!!!
def lex(codestring):
	codestring += '$'
	tokenlist = []

	i = 0
	while i < len(codestring):
		ch = codestring[i]
		if ch=='(':
			tokenlist.append( ('(',None) )
			i += 1
			continue
		elif ch==')':
			tokenlist.append( (')',None) )
			i += 1
			continue
		elif ch=='{':
			tokenlist.append( ('{',None) )
			i += 1
			continue
		elif ch=='}':
			tokenlist.append( ('}',None) )
			i += 1
			continue
		elif ch=='=':
			if i+1==len(codestring) or codestring[i+1]!='=':
				tokenlist.append( ('=',None) )
				i += 1
				continue
			else:
				tokenlist.append( ('==',None))
				i += 2
				continue
		elif ch==',':
			tokenlist.append( (',',None) )
			i += 1
			continue
		elif ch=='+':
			tokenlist.append( ('+',None) )
			i += 1
			continue
		elif ch=='-':
			tokenlist.append( ('-',None) )
			i += 1
			continue
		elif ch=='*':
			tokenlist.append( ('*',None) )
			i += 1
			continue
		elif ch=="/":
			tokenlist.append( ('/',None) )
			i += 1
			continue
		elif ch==";":
			tokenlist.append( (';',None) )
			i += 1
			continue
		elif ch=='>':
			if i+1==len(codestring) or codestring[i+1]!='=':
				tokenlist.append( ('>',None) )
				i += 1
				continue
			else:
				tokenlist.append( ('>=',None))
				i += 2
				continue
		elif ch=='<':
			if i+1==len(codestring) or codestring[i+1]!='=':
				tokenlist.append( ('<',None) )
				i += 1
				continue
			else:
				tokenlist.append( ('<=',None))
				i += 2
				continue
		elif isDigit(ch):
			j = i
			while j < len(codestring) and isDigit(codestring[j]):
				j += 1
			tokenstring = codestring[i:j]
			tokenlist.append( ("Constant", int(tokenstring)))
			i = j
			continue
		elif isAlpha(ch):
			"""
			예약어
			if else let print input
			"""
			j = i+1
			while j < len(codestring) and (isAlpha(codestring[j]) or isDigit(codestring[j])):
				j += 1
			tokenstring = codestring[i:j]
			if tokenstring=="if":
				tokenlist.append(("if",None))
			elif tokenstring=="else":
				tokenlist.append(("else",None))
			elif tokenstring=="let":
				tokenlist.append(("let",None))
			elif tokenstring=="print":
				tokenlist.append(("print",None))
			elif tokenstring=="input":
				tokenlist.append(("input",None))
			else:
				tokenlist.append( ("ID", tokenstring))
			i = j
			continue
		elif ch=='"':
			j = i+1
			while j < len(codestring) and codestring[j]!='"':
				j += 1
			j+=1
			if codestring[j-1]!='"':
				error(codestring,i)
			tokenstring = codestring[i+1:j-1]
			i = j

			tokenlist.append( ("String", tokenstring))
			continue
		elif ch=='#':
			while codestring[i]!='\n':
				i += 1
			i += 1
		elif ch=='\n' or ch=='\t' or ch==' ':
			i += 1
			continue
		elif ch=='$':
			break
		else :
			error(codestring,i)


	print("Lex OK")
	return tokenlist + [("$","END")]

def main():
	codefile = open(input("Enter code file path : "),"r",encoding="utf-8")
	tokenlist = lex(codefile.read())
	codefile.close()
	output = open("output/lex_result.txt","w",encoding="utf-8")
	for token in tokenlist:
		print(token)
		output.write(token[0] + "\t" + str(token[1])+"\n")
	output.close()

if __name__=="__main__":
	main()