import numpy as np
import itertools
from pyplasm import *

X_AXIS = np.array([1, 0, 0])
Y_AXIS = np.array([0, 1, 0])
Z_AXIS = np.array([0, 0, 1])

start_plane = np.array([0, 1, 0, 0])

def get_diff_vector(i1, i2, vertices):
    """
    Returns the vector between two points
    """
    p1, p2 = np.array([vertices[i1-1], vertices[i2-1]])
    return p2 - p1


def angle_between(vec1, vec2):
    l1 = np.linalg.norm(vec1)
    l2 = np.linalg.norm(vec2)
    return np.arccos(vec1.dot(vec2)/(l1*l2))
    

def inv_translation_mat(point):
    """
    Creates the inverse translation matrix relative to the given point
    """
    mat = np.identity(4)
    mat[0][3] = -point[0]
    mat[1][3] = -point[1]
    mat[2][3] = -point[2]
    return mat


def inv_x_rot_mat(angle):
    """
    Creates the inverse rotation matrix on the x-axis of the given angle
    """
    cos = np.cos(angle)
    sin = np.sin(angle)
    mat = np.identity(4)
    mat[1][1] = cos
    mat[1][2] = sin
    mat[2][1] = -sin
    mat[2][2] = cos
    return mat


def inv_z_rot_mat_vec(vec):
    """
    Creates the inverse rotation matrix on the z-axis of the given vector
    """
    vec = vec/np.linalg.norm(vec)
    cos = vec[0]
    sin = vec[1]
    mat = np.identity(4)
    mat[0][0] = cos
    mat[0][1] = sin
    mat[1][0] = -sin
    mat[1][1] = cos
    return mat


def intersection(plane1, plane2, plane3):
    """Gets the intersection between three planes"""
    A = np.array([plane1[:3], plane2[:3], plane3[:3]])
    B = -1*np.array([plane1[-1], plane2[-1], plane3[-1]])
    return list(np.linalg.solve(A,B))


def calc_next_prev_vertices(vi, vertices, faces):
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


def get_near_vertices(vi, vertices, faces):
    s = set(itertools.chain.from_iterable([f for f in faces if vi in f]))
    return [vertices[v-1] for v in list(set.difference(s, {vi}))]


def calc_points_average(points):
    """
    Calculates the component-wise average of the given vectors
    """
    points = np.array(points)
    mul = 1./points.shape[0]
    comps = points.T
    return mul*np.array([
        np.sum(comps[0]),
        np.sum(comps[1]),
        np.sum(comps[2])])


def get_roof_point(vi, vertices, faces, upper_plane, angle):
    """
    Get the point of the roof relative to the given one
    """
    vertices = np.array(vertices)
    
    point = vertices[vi-1]
    
    next_vi, prev_vi = calc_next_prev_vertices(vi, vertices, faces)
    next_vec = get_diff_vector(vi, next_vi, vertices)
    prev_vec = get_diff_vector(vi, prev_vi, vertices)
    
    pavg = calc_points_average(get_near_vertices(vi, vertices, faces))
    vavg = pavg - point
    
    v1 = np.cross(next_vec, Z_AXIS)
    v2 = np.cross(prev_vec, Z_AXIS)
    
    half_pi = np.pi/2
    c_next = 1 if (-half_pi <= angle_between(v1, vavg) <= half_pi) else -1
    c_prev = 1 if (-half_pi <= angle_between(v2, vavg) <= half_pi) else -1
    
    
    inv_t_mat = inv_translation_mat(point)
    
    next_trans = np.dot(inv_x_rot_mat(c_next*angle), inv_z_rot_mat_vec(next_vec))
    next_trans = np.dot(next_trans, inv_t_mat)
    
    prev_trans = np.dot(inv_x_rot_mat(c_prev*angle), inv_z_rot_mat_vec(prev_vec))
    prev_trans = np.dot(prev_trans, inv_t_mat)
    
    next_plane = np.dot(start_plane, next_trans)
    prev_plane = np.dot(start_plane, prev_trans)
    
    return intersection(next_plane, prev_plane, upper_plane), next_vi
    

def ggpl_workshop_09(vts, fcs, roof_height, angle):
    upper_plane = np.array([0, 0, 1, -roof_height])
    hpcs = []
    
    data = [get_roof_point(i, vts, fcs, upper_plane, angle)
        for i in range(1, len(vts)+1)]
    
    new_vts = [p for p,_ in data]
    print new_vts
    VIEW(MKPOL([new_vts,fcs,[1]]))
    
    for i in range(len(data)):
        nexti = data[i][1] - 1
        hpcs.append(MKPOL([
            [
                data[i][0], data[nexti][0],
                vts[i], vts[nexti]],
            [[1, 2, 3, 4]],
            [1]]))
    
    #print hpcs
    
    return STRUCT([
        STRUCT(hpcs),
        MKPOL([[p for p, _ in data], fcs, [1]])])

if __name__=='__main__':
    
    # L semplice
    vts = [
        [0,0,0], #1
        [5,0,0], #2
        [5,2,0], #3
        [2,2,0], #4
        [2,5,0], #5
        [0,5,0]] #6
    fcs = [
        [1,2,3,4],
        [1,4,5,6]]
    
    """
    # L smussata
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
    """
    
    """
    # Quadrati intersecati
    vts = [
        [0, 0, 0],
        [4, 0, 0],
        [4, 2, 0],
        [6, 2, 0],
        [6, 6, 0],
        [2, 6, 0],
        [2, 4, 0],
        [0, 4, 0]]
    fcs = [
        [1, 2, 3, 7, 8],
        [3, 4, 5, 6, 7]]
    """
    
    """
    # Stella
    vts = [
        [0, 0, 0],
        [3, 1, 0],
        [6, 0, 0],
        [5, 3, 0],
        [6, 6, 0],
        [3, 5, 0],
        [0, 6, 0],
        [1, 3, 0]]    
    fcs = [
        [1, 2, 8],
        [2, 3, 4, 6, 7, 8],
        [4, 5, 6]]
    """
    
    """
    # Profilo fabbrica
    # Errori segmenti
    vts = [
        [0, 0, 0],
        [6, 0, 0],
        [6, 2, 0],
        [4, 4, 0],
        [4, 2, 0],
        [2, 4, 0],
        [2, 2, 0],
        [0, 4, 0]]
    fcs = [
        [1, 2, 3, 5, 7],
        [3, 4, 5],
        [5, 6, 7],
        [1, 7, 8]]
    """
    VIEW(MKPOL([vts,fcs,[1]]))
    VIEW(ggpl_workshop_09(vts, fcs, 1, np.pi/6))
        
