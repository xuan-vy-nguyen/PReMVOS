with open("classImageNet.txt") as fimg:
    listImg = []
    while True:
        line = fimg.readline()
        if line == "":
            break
        listImg.append(line.split('\n')[0])

with open("classVOS.txt") as fvos:
    listVos = []
    while True:
        line = fvos.readline()
        if line == "":
            break
        listVos.append(line.split('\n')[0])

with open("classToTrain.txt","w") as fout:
    for element in listVos:
        if element not in listImg:
            fout.write(element + '\n')
