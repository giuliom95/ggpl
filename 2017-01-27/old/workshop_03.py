from pyplasm import *


def genStep():
    """Generates a unitary step"""
    return PROD([MKPOL([[[0,0],[1,1],[1,2],[0,2]],[[1,2,3,4]],[1]]),QUOTE([1])])


def genRun(numSteps):
    """Generates a single run of stairs of given steps.
    
    :param numSteps: The number of steps of the run.
    """
    hpcs = []
    for i in range(numSteps-1):
        hpcs.append(genStep())
        hpcs.append(T([1,2])([1,1]))
    hpcs.append(genStep())
    
    
    return STRUCT(hpcs)
    

def genRun2(numSteps):
    return T(1)(1)(STRUCT([
        T(1)(-1)(CUBE(1)),
        genRun(numSteps-1)
    ]))
    

def genTwoRuns(runNumSteps):
    """Generates two runs. One up another.
    
    :param numSteps: The number of steps of a single run.
    """
    return STRUCT([
            genRun(runNumSteps),
            T([1,2,3])([runNumSteps,runNumSteps,1]),
            S(1)(-1.0), #Flip on the x axis
            genRun(runNumSteps)
        ])


def genUnitaryStair(runNumSteps):
    """Generates a complete U-shaped stair.
    
    :param numSteps: The number of steps of a single run.
    """
    model = STRUCT([
            genTwoRuns(runNumSteps),
            T([1,2])([runNumSteps,runNumSteps])(CUBOID([2,1,2])),
            T(1)(-1.0),
            CUBE(1),
            T(2)(runNumSteps*2),
            T(3)(1),
            CUBE(1)
        ])
    return MAP([S1,S3,S2])(STRUCT([T(1)(1),model])) 

    
def ggpl_u_shaped_stairs(dx,dy,dz):
    """Generates a complete U-shaped stair using given dmension.
    The number of steps is determined by the dz param. 
    The steps will be ~22cm tall.
    
    :param dx: The stair dimension along the x-axis
    :param dy: The stair dimension along the y-axis
    :param dz: The stair dimension along the z-axis
    """
    tan = dz/(dx*2.0)
    if tan < 0.53:
        print('Parameters not valid: Too little steep')
        return
    elif tan > 0.72:
        print('Parameters not valid: Too steep')
        return
    
    runSteps = (dz / 2) // 0.22
    unitaryModel = genUnitaryStair(int(runSteps))
    modelSize = SIZE([1,2,3])(unitaryModel)
    return STRUCT([
            S(1)(dx/modelSize[0]),
            S(2)(dy/modelSize[1]),
            S(3)(dz/modelSize[2]),
            unitaryModel
        ])
