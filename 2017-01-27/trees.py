from pyplasm import *
import numpy as np
    
def tree():
    coords = [(2*np.pi*np.random.rand(2))-np.pi for i in range(60)]
    def fn(l):
        u,v = l
        cosu = np.cos(u)
        return [cosu*np.cos(v), cosu*np.sin(v), np.sin(u)]
    points = map(fn, coords)
    faces = [[i+1] for i in range(30)]
    
    trunk_height = np.random.rand()+1.5
    
    return T([1,2,3])([-.1,-.1,trunk_height])(STRUCT([
        S([1,2])([1.2, 1.2])(JOIN([MKPOL([points, faces, [1]])])),
        TEXTURE(['wood.jpg',True, True, 300,300, 0, .1,.1, 0,0])(
            S(3)(-1)(CUBOID([.2,.2,trunk_height])))
        ]))
        
if __name__=='__main__':
    VIEW(tree())
