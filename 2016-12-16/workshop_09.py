import numpy as np

def angle_between(vec1, vec2):
    l1 = np.linalg.norm(vec1)
    l2 = np.linalg.norm(vec2)
    return np.arccos(vec1.dot(vec2)/(l1*l2))

        
def calc_roof_v(v, alpha, beta, h):
    new_v = v[:]
    d = h / np.sin(beta)
    
    new_v[0] = d * np.cos(alpha)
    new_v[1] = d * np.sin(alpha)
    new_v[2] = h
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
     
    A = set([f[fix_pos(f.index(vi)+1, len(f))] for f in fs])
    B = set([f[fix_pos(f.index(vi)-1, len(f))] for f in fs])
    
    return list((A|B) - (set.intersection(A,B)))

    
def bisector(vc, v1, v2):
    
    def internal(s1, s2):
        
        vec1 = np.array([s1(v1) - s1(vc), s2(v1) - s2(vc)])
        vec2 = np.array([s1(v2) - s1(vc), s2(v2) - s2(vc)])
        axis = np.array([1, 0])
        
        a1 = angle_between(vec1, axis)
        a2 = angle_between(vec2, axis)
        
        return (a1 - a2) / 2 + min(a1, a2)
        
        """return angle_between(
            np.array([s1(v1) - s1(vc), s2(v1) - s2(vc)]),
            np.array([s1(v2) - s1(vc), s2(v2) - s2(vc)]))"""
            
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
    
    for i in range(1,8):
        v1, v2 = calc_near_vs(i, vts, fcs)
        #print vts[i-1], vts[v1-1], vts[v2-1]
        xy_angle = bisector(vts[i-1], vts[v1-1], vts[v2-1])(S1, S2)
        print 180*xy_angle/np.pi
        #print calc_roof_v(vts[i-1], xy_angle, np.pi/3, 1)
    
