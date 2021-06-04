import lexical_analyzer as LA
import syntax_analyzer as SA

def print_error(code,debug_data):
	if code==0:
		print("에러! 변수를 선언하지 않았습니다 :", debug_data)
	elif code==1:
		print("에러! 이미 선언된 변수를 재선언합니다 :", debug_data)
	elif code==2:
		print("에러! 숫자만 입력 가능합니다 :",debug_data)
	else:
		print("에러!",debug_data)
	exit(-1)

mem = {} #변수 저장하는 곳

def STMTS(node):
	if node.children[0].token[0]=="eps":
		return
	else:
		stmt_node = node.children[0]
		toktype = stmt_node.token[0]
		if toktype == "IfStmt":
			IFSTMT(stmt_node)
		elif toktype =="LetStmt":
			LETSTMT(stmt_node)
		elif toktype =="IOStmt":
			IOSTMT(stmt_node)
		elif toktype == "AssignStmt":
			ASSIGN(stmt_node)

	STMTS(node.children[1])

def ASSIGN(node):
	name = node.children[0].token[1]
	eval = EXP(node.children[2])
	if name not in mem:
		print_error(0,name)
	mem[name] = eval

def IFSTMT(node):
	eval = EXP(node.children[2])
	if eval!=0:
		STMTS(node.children[5])
	else:
		ELSESTMT(node.children[7])

def ELSESTMT(node):
	if node.children[0].token[0]=="eps":
		return
	
	STMTS(node.children[2])


def LETSTMT(node):
	name = node.children[1].token[1]
	if name in mem:
		print_error(1,name)
	else:
		mem[name] = 0
	
	if len(node.children)==5:
		eval = EXP(node.children[3])
		mem[name] = eval
	return 0

def IOSTMT(node):
	func = node.children[0].token[0]

	if func == "print":
		if node.children[2].token[0] == "EXP":
			print(EXP(node.children[2]))
		elif node.children[2].token[0] == "String":
			print(STRING(node.children[2]))
	elif func == "input":
		if node.children[4].token[0] == "String":
			print(STRING(node.children[4]),end='')
		
		name = node.children[2].token[1]
		if name not in mem:
			print_error(0,name)

		input_data = input()
		if not input_data.isdigit():
			print_error(2,input_data)
		mem[name] = int(input_data)

def EXP(node):
	if len(node.children)==1:
		return TERM(node.children[0])

	op = node.children[1].token[0]
	term1 = TERM(node.children[0])
	term2 = TERM(node.children[2])

	if op=="+":
		return term1+term2
	elif op=="-":
		return term1-term2

def TERM(node):
	if len(node.children)==1:
		return FACT(node.children[0])

	op = node.children[1].token[0]
	fact1 = FACT(node.children[0])
	fact2 = FACT(node.children[2])

	if op=="*":
		return fact1*fact2
	elif op=="/":
		return fact1//fact2

def FACT(node):
	if len(node.children)==1:
		return LOGI(node.children[0])
	
	op = node.children[1].token[0]
	logi1 = LOGI(node.children[0])
	logi2 = LOGI(node.children[2])

	if op==">":
		return 1 if logi1>logi2 else 0
	elif op=="<":
		return 1 if logi1<logi2 else 0
	elif op==">=":
		return 1 if logi1>=logi2 else 0
	elif op=="<=":
		return 1 if logi1<=logi2 else 0
	elif op=="==":
		return 1 if logi1==logi2 else 0

def LOGI(node):
	children = node.children
	if children[0].token[0] == "ID":
		return ID(children[0])
	elif children[0].token[0] == "Constant":
		return CONSTANT(children[0])
	elif children[1].token[0] == "EXP":
		return EXP(children[1])

def ID(node):
	name = node.token[1]
	if name not in mem:
		print_error(1,name)
	else:
		return mem[name]

def CONSTANT(node):
	return node.token[1]

def STRING(node):
	return node.token[1]

def run(parsetree):
	STMTS(parsetree)

def traverse_tree(node):
	print(node.token)
	if not node.children:
		return
	for child in node.children:
		traverse_tree(child)

def main():
	codefile = open(input("Enter code file path : "),"r",encoding="utf-8")
	tokenlist = LA.lex(codefile.read())
	codefile.close()

	parse_result = SA.lrparse(tokenlist)
	#traverse_tree(parse_result)
	run(parse_result)

if __name__=='__main__':
	main()