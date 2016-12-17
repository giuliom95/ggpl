import numpy as np

def angle_between(vec1, vec2):
    l1 = np.linalg.norm(vec1)
    l2 = np.linalg.norm(vec2)
    return np.arccos(vec1.dot(vec2)/(l1*l2))

def angle_coeff(vec):
    def intern(s1, s2):
        return np.arctan2(s2(vec),s1(vec))
    return intern

        
def calc_roof_v(v, alpha, beta, h):
    new_v = v[:]
    d = h / np.sin(beta)
    
    new_v[0] += d * np.cos(alpha)
    new_v[1] += d * np.sin(alpha)
    new_v[2] += h
    return new_v
    

def calc_near_vs(vi, vertices, faces):
    """
    Given vertex index, returns the indices of the
    near vertices of the roof
    """
    fs = [f for f in faces if vi in f] 
    
    def fix_pos(i, rg):
        if i < 0:
            i = rg - 1
        elif i >= rg:
            i = 0
        return i
     
    A = [f[fix_pos(f.index(vi)+1, len(f))] for f in fs]
    B = [f[fix_pos(f.index(vi)-1, len(f))] for f in fs]
    tutti = A + B
    return [v for v in tutti if not (v in A and v in B)]

    
def bisector(vc, v1, v2):
    
    def internal(s1, s2):
        
        print vc, v1, v2
        vec1 = np.array([s1(v1) - s1(vc), s2(v1) - s2(vc)])
        vec2 = np.array([s1(v2) - s1(vc), s2(v2) - s2(vc)])
        print vec1, vec2
        axis = np.array([1, 0])
        
        return angle_coeff(vec1+vec2)(s1, s2)
            
    return internal;


def ggpl_workshop_09():
    return None


if __name__=='__main__':
    
    from pyplasm import *
    
    vts = [
        [2, 0, 0], #1
        [5, 0, 0], #2
        [5, 3, 0], #3
        [3, 3, 0], #4
        [3, 5, 0], #5
        [0, 5, 0], #6
        [0, 2, 0]] #7
    fcs = [
        [1,2,3],
        [1,3,4],
        [1,4,7],
        [4,5,6,7]]
        
    hpc = MKPOL([vts, fcs, [1]])
    #VIEW(SKEL_1(hpc))
    
    new_vs = []
    for i in range(1,8):
        print i
        
        v1, v2 = calc_near_vs(i, vts, fcs)
        print v1, v2
        
        #print vts[i-1], vts[v1-1], vts[v2-1]
        
        xy_angle = bisector(vts[i-1], vts[v1-1], vts[v2-1])(S1, S2)
        if i == 4:
            
        
        print 180*xy_angle/np.pi
        
        new_vs += [calc_roof_v(vts[i-1], xy_angle, np.pi/3, 1)]
        print ''
        
    hpc2 = MKPOL([new_vs, fcs, [1]])
    VIEW(STRUCT([SKEL_1(hpc),SKEL_1(hpc2)]))
