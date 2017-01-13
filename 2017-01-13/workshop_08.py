from pyplasm import *

# There are some errors in the windows and the doors, but probably they come
#  from the poorly drawn SVG input.

DEF_THICKNESS = 3.5

def line_parser(filename):
    ret = []
    for line in open(filename):
        x1,y1,x2,y2 = line.rstrip().split(',')
        ret.append([float(x1),float(y1)])
        ret.append([float(x2),float(y2)])
    return ret


def gen_ext_walls_plan(filename, thickness):    
    verts = line_parser(filename)[::2]
    facets = [[i,i+1] for i in range(1,len(verts))]
    facets.append([len(verts),1])
    
    return OFFSET([thickness]*2)(MKPOL([verts,facets,[1]]))
    

def gen_int_walls_plan(filename, thickness):    
    verts = line_parser(filename)
    facets = [[i,i+1] for i in range(1,len(verts),2)]
    
    return OFFSET([thickness]*2)(MKPOL([verts,facets,[1]]))

    
def gen_walls(filename, thickness, height, external):
    if(external):
        return PROD([
            gen_ext_walls_plan(filename, thickness),
            Q(height)
        ])
    else:
        return PROD([
            gen_int_walls_plan(filename, thickness),
            Q(height)
        ])   

def gen_windows(filename, height, foot_height, thickness=DEF_THICKNESS):
    ret = []
    verts = line_parser(filename)
    couples = [[i,i+1] for i in range(1,len(verts),2)]
    
    for (i, j) in couples:
        delta_x = abs(verts[i-1][0] - verts[j-1][0])
        delta_y = abs(verts[i-1][1] - verts[j-1][1])
        if delta_x > delta_y:
            ret.append(
                T([1,2,3])([
                    verts[i-1][0],
                    verts[i-1][1] - (thickness/4),
                    foot_height
                ])(CUBOID([delta_x,thickness,height]))
            )
        else:
            ret.append(
                T([1,2,3])([
                    verts[i-1][0] - (thickness/4),
                    verts[i-1][1],
                    foot_height
                ])(CUBOID([thickness,delta_y,height]))
            )
        
    return STRUCT(ret)
    
def gen_doors(filename, height, thickness=DEF_THICKNESS):
    return gen_windows(filename, height, 0, thickness)


if __name__=='__main__':
    struttura = S([2])([-1])(DIFFERENCE([
        STRUCT([
            gen_walls('esterni.lines', 2, 12, True),
            gen_walls('interni.lines', 2, 12, False)
        ]),
        STRUCT([
            gen_windows('finestre.lines', 8, 2),
            gen_doors('porte.lines', 8)
        ])
    ]))


    VIEW(struttura)

