import json

filename = "games\\frogger\\frogger.c"

text = open(filename, 'r').read()

text = text.replace(' ','')

text = text.replace('\\\\','\n\\\\')

text = text.split('\n')

for line in text:
    print (len(line) , line)
    if len(line)<1:# or (line[0] == '/' and line[1] == '/'):
        text.remove(line)

for line in text:
    print(line)
    pass
