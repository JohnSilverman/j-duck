import lexical_analyzer as LA
import lrtable.parseTable as PT

PRODUCTION_RULE = \
"""S -> Stmts
Stmts -> IfStmt Stmts
Stmts -> LetStmt Stmts
Stmts -> IOStmt Stmts
Stmts -> AssignStmt Stmts
Stmts -> EXP Stmts
Stmts -> ''
AssignStmt -> ID = EXP ;
IfStmt -> if ( EXP ) { Stmts } ElseStmt
ElseStmt -> else { Stmts }
ElseStmt -> ''
LetStmt -> let ID ;
LetStmt -> let ID = EXP ;
IOStmt -> print ( EXP ) ;
IOStmt -> print ( String ) ;
IOStmt -> input ( ID ) ;
IOStmt -> input ( ID , String ) ;
EXP -> TERM + TERM
EXP -> TERM - TERM
EXP -> TERM
TERM -> FACT * FACT
TERM -> FACT / FACT
TERM -> FACT
FACT -> LOGI > LOGI
FACT -> LOGI < LOGI
FACT -> LOGI >= LOGI
FACT -> LOGI <= LOGI
FACT -> LOGI == LOGI
FACT -> LOGI
LOGI -> ID
LOGI -> Constant
LOGI -> ( EXP )"""

#생성규칙을 리스트형태로
#PRODUCTION_RULE[i][0]이 생성규칙 왼쪽이고 [1]이 오른쪽
PRODUCTION_RULE = PRODUCTION_RULE.split("\n")
for i in range(len(PRODUCTION_RULE)):
	PRODUCTION_RULE[i] = PRODUCTION_RULE[i].split("->")
	PRODUCTION_RULE[i][0] = PRODUCTION_RULE[i][0].strip()
	PRODUCTION_RULE[i][1] = PRODUCTION_RULE[i][1].split()
	if PRODUCTION_RULE[i][1]==["''"]:
		PRODUCTION_RULE[i][1]=[]
	#print(PRODUCTION_RULE[i])

def error(expected,token):
	print("SyntaxError : Expected",expected,"but",token,"appeared")
	exit(-1)

def reduce_err(rule):
	print("Reduce error",PRODUCTION_RULE[rule])
	exit(-1)

#Parse Tree
class Node:
	def __init__(self):
		self.token = None
		self.parent = None
		self.children = []

	def set_token(self,token):
		self.token = token

	def __repr__(self):
		return str(self.token)

	def add_child(self,node):
		self.children.append(node)

symbollist = PT.get_symbols()
nodestack = []

#핵심 파싱함수
def lrparse(tokenlist):

	stack = [0]

	lrtable = PT.get() 
	#lrtable[STATE][SYMBOL]=ACTION
	
	def shift(nxt_token, state):
		stack.append(nxt_token)
		stack.append(state)

		newnode = Node()
		newnode.set_token(nxt_token)
		nodestack.append(newnode)

	def reduce(rule):
		popnum = len(PRODUCTION_RULE[rule][1])
		left_nonterminal = PRODUCTION_RULE[rule][0]
		newtoken = (left_nonterminal,None)

		newnode = Node()
		newnode.set_token(newtoken)
		#print("NODESTACK",nodestack)

		tmp = []
		for i in range(popnum):
			stack.pop() # state
			tmp.append(stack.pop()[0])

			popnode = nodestack.pop()
			newnode.children.insert(0, popnode)
			#print(popnode,"added to",newnode)
		nodestack.append(newnode)
		#print("TRAVERSE")
		#traverse_tree(newnode)

		if popnum==0:
			epsnode = Node()
			epsnode.set_token(("eps",None))
			newnode.add_child(epsnode)

		if tmp[::-1]!=PRODUCTION_RULE[rule][1]:
			# print("STACK",stack)
			# print("TMP",tmp[::-1])
			# print("RULE",PRODUCTION_RULE[rule][1])
			reduce_err(rule)

		current_state = stack[-1]
		stack.append(newtoken)

		if left_nonterminal not in lrtable[current_state]:
			reduce_err(rule)
		else:
			stack.append(int(lrtable[current_state][left_nonterminal])) #goto

	output = open("output/parse_result.txt","w",encoding="utf-8")

	tp = 0 #tokenlist pointer
	while True:
		current_state = stack[-1]

		#print("STACKLOG",stack)

		nxt_token = tokenlist[tp]
		#print("next token=",nxt_token)

		output.write("STATE "+str(current_state)+"\t'"+nxt_token[0]+"'\tSTACK "+str(stack)+"\n")

		if nxt_token[0] not in lrtable[current_state]:
			# print("STATE",current_state)
			# print("NEXT TOKEN",nxt_token[0])
			error(list(lrtable[current_state].keys()),nxt_token[0])
		else:
			action = lrtable[current_state][nxt_token[0]]

			if "s" in action:
				shiftto = int(action[1:])
				shift(nxt_token,shiftto)

				tp += 1
			elif "r" in action:
				reduceto = int(action[1:])
				reduce(reduceto)
			elif action == "acc":
				# for symbol in symbolcount:
				# 	print(symbol,symbolcount[symbol])
				#print(nodestack)
				print("Syntax OK")
				return nodestack[-1]

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

	parse_result = lrparse(tokenlist)
	traverse_tree(parse_result)

if __name__=='__main__':
	main()