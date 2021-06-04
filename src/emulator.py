import lexical_analyzer as LA
import syntax_analyzer as SA

def print_error(code,debug_data):
	if code==0:
		print("에러! 변수를 선언하지 않았습니다 :", debug_data)
	elif code==1:
		print("에러! 이미 선언된 변수를 재선언합니다 :", debug_data)
	else:
		print("에러!",debug_data)

mem = {} #변수 저장하는 곳

def LETSTMT(node):
	name = node.children[1].token[1]
	if name in mem:
		print_error(1,name)
		return -1
	else:
		mem[name] = 0
	
	# if len(node.children)==5:
	# 	eval = EXP(node.children[3])
	# 	mem[name] = eval
	return 0

def ASSIGN(name,value):
	if name in mem:
		mem[name] = value
	else:
		print_error(0,name)
	return 0

def LOGI(node):
	token = node.token
	if token[0]=="ID":
		if token[1] not in mem:
			print_error(1,token[1])
			return -1
		else:
			return mem[token[1]]
	elif token[0]=="Constant":
		return token[1]
	#TODO : (EXP) 추가

def 

def run(parsetree):
	pass

def main():
	codefile = open(input("Enter code file path : "),"r",encoding="utf-8")
	tokenlist = LA.lex(codefile.read())
	codefile.close()

	parse_result = SA.lrparse(tokenlist)
	res = run(parse_result)
	print("Program returned with value",res)

if __name__=='__main__':
	main()