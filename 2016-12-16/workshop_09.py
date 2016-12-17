import numpy as np
from pyplasm import *

X_AXIS = np.array([1, 0, 0])
Y_AXIS = np.array([0, 1, 0])
Z_AXIS = np.array([0, 0, 1])

def find_point(a, b, c, d):
    v = np.array([a, b, c])
    k = -1.*d/(a**2 + b**2 + c**2)
    return k*v


def plane_hpc(coeffs, dim=1):
    start_point = find_point(*coeffs)
    n = coeffs[:3]
    points = [
        list(start_point + np.cross(n, dim*X_AXIS)),
        list(start_point + np.cross(n, dim*Y_AXIS)),
        list(start_point + np.cross(n, dim*Z_AXIS)),
        list(start_point + np.cross(n, -dim*X_AXIS)),
        list(start_point + np.cross(n, -dim*Y_AXIS)),
        list(start_point + np.cross(n, -dim*Z_AXIS))]
    
    faces = [[i+1] for i in range(len(points))] 
    
    return JOIN([MKPOL([points, faces, [1]])])
    
    
def det_steep(vic, vi1, vi2, vs):
    xc, yc, _ = vs[vic-1]
    x1, y1, _ = vs[vi1-1]
    x2, y2, _ = vs[vi2-1]
    dx1 = x1 - xc
    dx2 = x2 - xc
    dy1 = y1 - yc
    dy2 = y2 - yc
    
    print 'Delta:',dx1, dy1, dx2, dy2
    
    #1
    if dx2 > 0 and dy1 > 0:
        print 1
        return 1, 1
    #2
    if dx1 > 0 and dy2 > 0:
        print 2
        return -1, -1
    #3
    if dx2 < 0 and dy1 > 0:
        print 3
        return -1, 1
    #4
    if dx1 < 0 and dy2 > 0:
        print 4
        return -1, 1
    #5
    if dx1 < 0 and dy2 < 0:
        print 5
        return -1, -1
    #6
    if dx2 < 0 and dy1 < 0:
        print 6
        return 1, 1
    #7
    if dx2 > 0 and dy1 < 0:
        print 7
        return 1, 1
    #8
    if dx1 > 0 and dy2 < 0:
        print 8
        return -1, 1
    
    return None


def plane_through_xyvector(vec, angle):
    if vec[1] != 0:
        plane = np.array([1.,0,0,0])
        plane[1] = plane[0] * -(vec[0]/vec[1])
    else:
        plane = np.array([0,1.,0,0])
        
    plane[2] = np.linalg.norm(plane[:2])*np.tan(angle)
    return plane


def translation_mat(dx, dy, dz):
    """
    Creates the translation matrix relative to the given vector
    """
    mat = np.identity(4)
    mat[0][3] = dx
    mat[1][3] = dy
    mat[2][3] = dz
    return mat


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


def build_roof_plane(vi1, vi2, vs, angle):
    plane = plane_through_xyvector(
        [vts[vi1-1][0]-vts[vi2-1][0], vts[vi1-1][1]-vts[vi2-1][1]],
        angle)
    return plane.dot(np.linalg.inv(translation_mat(*vts[vi1-1])))


def intersection(plane1, plane2, plane3):
    A = np.array([plane1[:3], plane2[:3], plane3[:3]])
    B = -1*np.array([plane1[-1], plane2[-1], plane3[-1]])
    return list(np.linalg.solve(A,B))


if __name__=='__main__':

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
    
    roof_top = [0,0,1,-.5]
    new_vts = []
    to_view = []
    for vic in range(1,len(vts)+1):
    #for vic in [4]:
        vi1, vi2 = calc_near_vs(vic, vts, fcs)
        
        print 'Punto:',vic
        angle = np.pi/6
        c1, c2 = det_steep(vic, vi1, vi2, vts)
        #, c1, c2
        
        plane1 = build_roof_plane(vic, vi1, vts, c1*angle)
        plane2 = build_roof_plane(vic, vi2, vts, c2*angle)
        
        #to_view += [plane_hpc(plane1, 4), plane_hpc(plane2, 4)] 
        new_vts += [intersection(roof_top, plane1, plane2)]
    
    
    to_view = [
        SKEL_1(MKPOL([vts, fcs, [1]])), 
        SKEL_1(MKPOL([new_vts, fcs, [1]]))]
    
     
    VIEW(STRUCT(to_view))
    """
    toview = [
        plane_hpc(plane1, 2),
        plane_hpc(plane2, 2),
        plane_hpc(roof_top, 2)]
    
    VIEW( STRUCT(toview) )
    """
    
