from lexical import scanner

with open("testfile.txt", 'r') as txt:
    code = txt.read()

scan = scanner(code)
scan.lexical()
token = scan.tokens

if token[-1]:
    for i in token:
        print(i)
else:
    print("Error occurred in lexical analysis")