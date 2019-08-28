with open('metaImageNet.txt') as f:
    with open('classImageNet.txt','w') as fo:
        prec = ''
        while True:
            c = f.read(1)
            if c == ' ' and prec == ',':
                fo.write('\n')
            elif c == ' ' and prec!= ',':
                fo.write('\n')
            elif c != ' ' and c != ',':
                fo.write(c)
            prec = c
            if c == '':
                break
    