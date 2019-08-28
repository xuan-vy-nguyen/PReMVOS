import json

with open('meta.json') as f:
    data = json.load(f)['videos']
    dataOutput =[]
    with open('findObjectID.txt',"w") as output:
        for namevideo in data:
            for element in data[namevideo]['objects']:
                dataOutput.append(namevideo)
                dataOutput.append(element)
                dataOutput.append(data[namevideo]['objects'][element]['category'])
        i = 0
        while i < len(dataOutput):
            output.write(dataOutput[i] + ','+ dataOutput[i+1] + ','+ dataOutput[i+2] + '\n')
            i+=3
