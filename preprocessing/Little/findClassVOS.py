import json

with open('meta.json') as f:
    data = json.load(f)['videos']
    dataOutput = []
    with open('classVOS.txt',"w") as output:
        for namevideo in data:
            for element in data[namevideo]['objects']:
                if data[namevideo]['objects'][element]['category'] not in dataOutput:
                    dataOutput.append(data[namevideo]['objects'][element]['category'])

        for element in dataOutput:
            output.write(element + '\n')
