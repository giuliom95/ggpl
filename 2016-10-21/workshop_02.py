from larlib import *
import frameGenerator

def strToParameters(string):
    cells = string.split(',')
    final = []
    for element in cells:
        final.append([float(num) for num in element.split(';')])
    return final
    
def generateListElement(param):
    """Given a list, it returns a list of pyPlasm objects"""
    
    if len(param) == 1:
        return [T(i+1)(param[0][i]) for i in range(len(param[0]))]
    else:
        return [frameGenerator.createStructure(param[0],param[1],param[2],param[3],'pillars>beams')]
        
def stringsToCG(lines):
    """Given a list of strings returns a list of pyPlasm functions"""
    
    ret = []
    for line in lines:
        ret.extend(generateListElement(strToParameters(line)))
    return ret
    
def ggpl_bone_structure(file_name):
    with open(file_name) as csv:
        return STRUCT(stringsToCG(csv.readlines()))

