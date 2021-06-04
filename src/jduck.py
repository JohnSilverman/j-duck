import lexical_analyzer as LA
import syntax_analyzer as SA
import emulator as EM

codefile = open(input("Enter code file path : "),"r",encoding="utf-8")
tokenlist = LA.lex(codefile.read())
codefile.close()
parse_result = SA.lrparse(tokenlist)
#EM.traverse_tree(parse_result)
EM.run(parse_result)