import json

CLASS = ['leopard']
CLASS2= ['parrot']

with open('meta.json') as f:
    data = json.load(f)['videos']
    listVideo =[]
    with open('findObjectID.txt',"w") as output:
        for namevideo in data:
            for element in data[namevideo]['objects']:
                if data[namevideo]['objects'][element]['category'] in CLASS and namevideo not in listVideo:
                    listVideo.append(namevideo)

        for i in range(len(listVideo)):
            output.write(listVideo[i] + '\n')
