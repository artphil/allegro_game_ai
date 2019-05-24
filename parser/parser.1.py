import json

filename = "games\\frogger\\frogger.c"

text = open(filename, 'r').read()

lib = []
# Retira comentarios e bibliotecas
comment = True
while comment:
        comment = False
        s = text.find('/*')
        if s > -1:
                comment = True
                e = text.find('*/',s)
                text = text[:s]+text[e+2:]
     
        s = text.find('//')
        if s > -1:
                comment = True
                e = text.find('\n',s)
                text = text[:s]+text[e:]     
        
        s = text.find('#include')
        if s > -1:
                comment = True
                e = text.find('\n',s)
                lib.append(text[s+8:e].strip())
                text = text[:s]+text[e:]  

print (lib)
# Retira catacteres invalidos
invalids  = ['\n','\t']

for s in invalids:
        text = text..strip('\n\t')

# Destaca caracteres validos
starts  = ['[','{','(']
ends    = [']','}',')']
others  = [';',',','.','/','=','+','-']
valids  = starts+ends+others

for s in valids:
        text = text.replace(s,' '+s+' ')

text =  [w for w in text.split(' ') if len(w) > 0 ]             

print(text)

for line in text:
#     print(line)
    pass
