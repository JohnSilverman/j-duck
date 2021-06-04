# j-duck

시험기간에 너무 심심해서 구현해본 간단한 프로그래밍 언어

구성
1. 어휘 분석기
2. 구문 분석기 
3. 시뮬레이터

기능
1. 변수 선언 let 
2. if-else
3. 자료형 : 정수 
4. 연산자 : 사칙연산, 비교 
5. 입출력 : print, input 

BNF 정의 \
S -> Stmts \
Stmts -> IfStmt Stmts \
Stmts -> LetStmt Stmts \
Stmts -> IOStmt Stmts \
Stmts -> AssignStmt Stmts \
Stmts -> EXP Stmts \
Stmts -> '' \
AssignStmt -> ID = EXP ; \
IfStmt -> if ( EXP ) { Stmts } ElseStmt <br />
ElseStmt -> else { Stmts } <br />
ElseStmt -> '' <br />
LetStmt -> let ID ; <br />
LetStmt -> let ID = EXP ; <br />
IOStmt -> print ( EXP ) ; \
IOStmt -> print ( String ) ; <br/>
IOStmt -> input ( ID ) ; \
IOStmt -> input ( ID , String ) ; \
EXP -> TERM + TERM \
EXP -> TERM - TERM \
EXP -> TERM \
TERM -> FACT * FACT \
TERM -> FACT / FACT \
TERM -> FACT \
FACT -> LOGI > LOGI \
FACT -> LOGI < LOGI \
FACT -> LOGI >= LOGI \
FACT -> LOGI <= LOGI \
FACT -> LOGI == LOGI \
FACT -> LOGI \
LOGI -> ID \
LOGI -> Constant <br />
LOGI -> ( EXP )

ID -> Alphabet AlphaNum* \
Constant -> 정수 숫자 \
Alphabet -> 영어알파벳이랑 언더스코어 \
AlphaNum -> Alphabet이랑 Digit \
String -> Alphabet+ \
Digit -> 0부터 9까지 <br />
