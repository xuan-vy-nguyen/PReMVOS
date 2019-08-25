import os
import glob
import numpy
from sh import cd 

RefinedPath = '../../../Downloads/PReMVOS/output/intermediate/refined_proposals/'
CombinedPath = '../combined_proposals/'

if __name__ == '__main__':
    dictRefined = {}
    os.chdir(RefinedPath)
    for name in os.listdir("."): 
        if os.path.isdir(name):
            count=0
            for fileName in os.listdir(name):
                count+=1
            dictRefined[name] = count
    dictCombined = {}
    os.chdir(CombinedPath)
    for name in os.listdir("."):
        if os.path.isdir(name):
            count=0
            for fileName in os.listdir(name):
                count+=1
            dictCombined[name]=count
    
    os.chdir("../../../../../Documents/PReMVOS/preprocessing/")
    f = open("notSolve.txt", "w")
    for element in dictCombined:
        if (dictCombined[element] != dictRefined[element]):
                f.write(element+'\n')
    f.close()

