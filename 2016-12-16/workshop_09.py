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
    return [v for v in tutti if not (v in A and v in B)][::-1]


def build_roof_plane(vi1, vi2, vs, angle):
    """
    Builds a plane given two points and an angle
    """
    plane = plane_through_xyvector(
        [vts[vi1-1][0]-vts[vi2-1][0], vts[vi1-1][1]-vts[vi2-1][1]],
        angle)
    return plane.dot(np.linalg.inv(translation_mat(*vts[vi1-1])))


def intersection(plane1, plane2, plane3):
    """Gets the intersection between three planes"""
    A = np.array([plane1[:3], plane2[:3], plane3[:3]])
    B = -1*np.array([plane1[-1], plane2[-1], plane3[-1]])
    return list(np.linalg.solve(A,B))


def get_vector(i1, i2, vertices):
    """
    Returns the vector between two points
    """
    p1, p2 = np.array([vertices[i1-1], vertices[i2-1]])
    return p2 - p1
    
    
def get_coeffs(v):
    """
    Black magic
    """
    return -np.sign(v[0]), np.sign(v[1])


def ggpl_workshop_09(vts, fcs, roof_height, angle):
    roof_top = [0,0,1,-roof_height]
    new_vts = []
    
    for vic in range(1,len(vts)+1):
        vi1, vi2 = calc_near_vs(vic, vts, fcs)
        
        v1 = get_vector(vi1, vic, vts)
        v2 = get_vector(vic, vi2, vts)
        c1, c2 = get_coeffs(v1 + v2)
        print v1, v2, v1+v2, c1, c2
        
        plane1 = build_roof_plane(vic, vi1, vts, c1*angle)
        plane2 = build_roof_plane(vic, vi2, vts, c2*angle)
        
        new_vts += [intersection(roof_top, plane1, plane2)]
        
    return MKPOL([new_vts, fcs, [1]])


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
    
    hpc = ggpl_workshop_09(vts, fcs, .8, np.pi/6)
    
    to_view = [
        SKEL_1(MKPOL([vts, fcs, [1]])), 
        SKEL_1(hpc)]
    
     
    VIEW(STRUCT(to_view))
    
