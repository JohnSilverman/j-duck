def get_table(lines): 

	symbols = "if	(	)	{	}	else	let	ID	;	=	print	String	input	,	+	-	*	/	>	<	>=	<=	==	Constant	$	S	Stmts	IfStmt	ElseStmt	LetStmt	IOStmt	EXP	TERM	FACT	LOGI".split("\t")
	print("SYMBOLS",symbols)

	lrtable = []
	for line in lines:
		line = line.strip().replace(" ","S").split("\t")
		lrtable.append({})

		del line[0]
		i = -1
		for action in line:
			i += 1
			if action=='S':
				continue
			else:
				lrtable[-1][symbols[i]] = action

	for i in range(71):
		print("STATE",i)
		print(lrtable[i])
	
	return lrtable

if __name__=="__main__":
	file = open("parsing table.txt","r")
	lines = file.readlines()
	file.close()

	lrtable = get_table(lines)