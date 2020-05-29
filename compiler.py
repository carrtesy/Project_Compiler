from lexical import scanner

with open("testfile.txt", 'r') as txt:
    code = txt.read()

scan = scanner(code)
scan.lexical()
token = scan.tokens

for i in token:
    print(i)
