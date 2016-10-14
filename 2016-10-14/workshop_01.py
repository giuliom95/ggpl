from larlib import *

def createPillarBases (pillarSection, pillarDistances) :

	res = []
	invertedPillarDistances = [-i for i in pillarDistances] #Inverts the elements of the list
	for i in invertedPillarDistances:
		res.append(pillarSection[1])
		res.append(i)
	res.append(pillarSection[1])
	
	return PROD([QUOTE([pillarSection[0]]),QUOTE(res)])

def erectPillars (pillarBases, beamSection, beamDistances) :
	res = []
	for i in beamDistances:
		res.append(i)
		res.append(beamSection[1]*-1)
	
	return PROD([pillarBases,QUOTE(res)])
	
def calculateModelWidth (pillarSection, pillarDistances) :
	width = 0
	for i in pillarDistances:
		width += i
	width += pillarSection[1]*(len(pillarDistances)+1)
	return width
	
def createBeams (beamSection, beamDistances, modelWidth) :
	model = QUOTE([beamSection[0]])
	model = PROD([model,QUOTE([modelWidth])])
	res = []
	
	invertedBeamDistances = [-i for i in beamDistances] #Inverts the elements of the list
	for i in invertedBeamDistances:
		res.append(i)
		res.append(beamSection[1])
	
	return PROD([model,QUOTE(res)])
	
def createStructure (beamSection, pillarSection, beamDistances, pillarDistances) :
	pillarBases = createPillarBases(pillarSection, pillarDistances)
	pillars = erectPillars(pillarBases, beamSection, beamDistances)
	modelWidth = calculateModelWidth(pillarSection, pillarDistances)
	beams = createBeams(beamSection, beamDistances, modelWidth)
	model = STRUCT([pillars,beams])
	model = STRUCT([T(1)(pillarSection[0]/-2.0),model])
	return STRUCT([T(2)(pillarSection[1]/-2.0),model])
	
pillarDistances = [3, 2, 2]
beamDistances = [4, 2, 2]
pillarSection = (0.5, 0.5)
beamSection = (0.5, 0.7)

model = createStructure(beamSection, pillarSection, beamDistances, pillarDistances)
VIEW(model)
