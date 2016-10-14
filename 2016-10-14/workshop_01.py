from larlib import *

def createPillarBases (pillarSection, pillarDistances) :
	"""Create the pillars' bases as a 2D polyhedra.
	Returns: pyplasm.xgepy.Hpc
	
	Keyword arguments:
	pillarSection -- (px,py) - Section of a pillar
	pillarDistances -- [dy1, dy2, ... ] - Pillars' distances 
	"""
	
	tempList = []
	invertedPillarDistances = [-i for i in pillarDistances] #Inverts the elements of the list
	for i in invertedPillarDistances:
		tempList.append(pillarSection[1])
		tempList.append(i)
	tempList.append(pillarSection[1])
	
	return PROD([QUOTE([pillarSection[0]]),QUOTE(tempList)])


def erectPillars (pillarBases, beamSection, beamDistances, fillHoles) :
	"""Create the pillars as a 3D polyhedra.
	Returns: pyplasm.xgepy.Hpc
		
	Keyword arguments:
	pillarBases -- pyplasm.xgepy.Hpc - 2D polyhedra of the pillars' bases
	beamSection -- (bx,bz) - Section of a beam
	beamDistances -- [hz1, hz2, ... ] - Beams' distances 
	fillHoles -- bool - Controls if the space where the beams pass must be filled or not
	"""
	
	beamSectMultiplier = 1 if fillHoles else -1
	tempList = []
	for i in beamDistances:
		tempList.append(i)
		tempList.append(beamSection[1]*beamSectMultiplier)
	
	return PROD([pillarBases,QUOTE(tempList)])
	
	
def createBeamsQuote (pillarSection, pillarDistances, fillHoles) :
	"""Create the QUOTE (a 1D polyhedra) of the beams.
	Returns: pyplasm.xgepy.Hpc
	
	Keyword arguments:
	pillarSection -- (px,py) - Section of a pillar
	pillarDistances -- [dy1, dy2, ... ] - Pillars' distances 
	fillHoles -- bool - Controls if the space where the pillars pass must be filled or not
	"""
	
	beamSectMultiplier = 1 if fillHoles else -1
	tempList = []
	for i in pillarDistances:
		tempList.append(pillarSection[1]*beamSectMultiplier)
		tempList.append(i)
	tempList.append(pillarSection[1]*beamSectMultiplier)
	
	return QUOTE(tempList)
	
	
def createBeams (beamsQuote, beamSection, beamDistances) :
	"""Create the pillars as a 3D polyhedra.
	Returns: pyplasm.xgepy.Hpc
	
	Keyword arguments:
	beamsQuote -- pyplasm.xgepy.Hpc - 1D polyhedra of the QUOTE of the beams
	beamSection -- 	(bx,bz) - Section of a beam
	beamDistances -- [hz1, hz2, ... ] - Beams' distances 
	"""
	
	bases = PROD([QUOTE([beamSection[0]]),beamsQuote])
	
	tempList = []
	
	invertedBeamDistances = [-i for i in beamDistances] #Inverts the elements of the list
	for i in invertedBeamDistances:
		tempList.append(i)
		tempList.append(beamSection[1])
	
	return PROD([bases,QUOTE(tempList)])


def createStructure (beamSection, pillarSection, beamDistances, pillarDistances, priority) :
	"""Generates a parametric model of a building structure in reinforced concrete.
	Returns: pyplasm.xgepy.Hpc
	
	Keyword arguments:
	beamSection -- 	(bx,bz) - Section of a beam
	pillarSection -- (px,py) - Section of a pillar
	beamDistances -- [hz1, hz2, ... ] - Beams' distances
	pillarDistances -- [dy1, dy2, ... ] - Pillars' distances
	priority -- str - If 'pillars>beams' is passed, beams are interrupted where pillars pass. Otherwise pillars are interrupted where beams pass.
	"""

	fillPillarsHoles = priority=='pillars>beams'
	
	pillarBases = createPillarBases(pillarSection, pillarDistances)
	pillars = erectPillars(pillarBases, beamSection, beamDistances, fillPillarsHoles)
	beamsQuote = createBeamsQuote(pillarSection, pillarDistances, not fillPillarsHoles)
	beams = createBeams(beamsQuote, beamSection, beamDistances)
	
	pillars = STRUCT([T(1)(pillarSection[0]/-2.0),T(2)(pillarSection[1]/-2.0),pillars])
	beams = STRUCT([T(1)(beamSection[0]/-2.0),T(2)(pillarSection[1]/-2.0),beams])

	return STRUCT([pillars,beams])
	
pillarDistances = [4, 2.5, 2.5]
beamDistances = [4, 2, 2]
pillarSection = (0.4, 0.4)
beamSection = (0.3, 0.4)

model = createStructure(beamSection, pillarSection, beamDistances, pillarDistances, 'pillars>beams')
VIEW(model)
