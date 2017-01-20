import os
from pyplasm import *
import numpy as np
import workshop_08 as w8    # .lines files utilities
import workshop_07 as w7    # Windows
import workshop_03 as w3    # Stairs

def line_parser(path):
    """
    Parses a .lines file into a list of couples of points (as 4 elems lists)
    """
    lines = []
    with open(path, 'r') as input:
        lines = [line.rstrip().split(',') for line in input]
        lines = [
            [[float(x1), float(y1)],
            [float(x2), float(y2)]] 
                for x1, y1, x2, y2 in lines]
    return lines


def fit_model_into_box(model, dx, dy, dz):
    """
    Scales a model inside the given box
    """
    modelSize = SIZE([1,2,3])(model)
    return STRUCT([
            S(1)(dx/modelSize[0]),
            S(2)(dy/modelSize[1]),
            S(3)(dz/modelSize[2]),
            model
        ])


def gen_floor(path, thickness):
    """
    Generates the floor from given file path.
    File pointed by the given path must be a .lines file.
    The input must describe a convex polygon.
    """
    lines = line_parser(path)
    vertices = [p for p, _ in lines]
    face = range(1, len(lines)+1)
    return PROD([
        MKPOL([vertices, [face], [1]]),
        Q(thickness)
    ])

    
def gen_windows(path, fn, height):
    """
    Given a .lines file and a function, for every line in the file
    generates a window using the passed function
    """
    lines = np.array(line_parser(path))
    hpcs = []
    for p1, p2 in lines:
        v = p2-p1
        v_len = np.linalg.norm(v)
        angle = np.arctan2(v[1], v[0])
        hpcs.append(
            STRUCT([
                T([1, 2])(p1),
                R([1, 2])(angle),
                MAP([S1, S3, S2]),
                fn(v_len, height, 1)
            ]))
    return STRUCT(hpcs)
    

def gen_doors(path, fn, height):
    """
    Given a .lines file and a function, for every line in the file
    generates a door and a doorway using the passed function
    """
    lines = np.array(line_parser(path))
    hpcs = []
    boxes = []
    for p1, p2 in lines:
        v = p2-p1
        v_len = np.linalg.norm(v)
        angle = np.arctan2(v[1], v[0])
        hpc = STRUCT([
                S(3)(-1),
                T(3)(-height),
                T([1, 2])(p1),
                R([1, 2])(angle),
                MAP([S1, S3, S2]),
                fn(v_len, height, 1)])
        hpcs.append(hpc)
        boxes.append(BOX([1,2,3])(hpc))
    doors = STRUCT(hpcs)
    doorways = STRUCT(boxes)
    return doors, doorways
    
def gen_stairs_foot(path):
    """
    Given a .lines file generates the position of a foot of a staicase
    """
    lines = line_parser(path)
    return lines[0]
    

def gen_stairs(lower_foot, upper_foot):
    """
    Generates a staircase and a cube given the two foots
    """
    lp1, lp2, lh = lower_foot
    up1, up2, uh = upper_foot
    lo = np.array(lp1 + [lh])
    hi = np.array(up2 + [uh])
    
    cube_dim = hi-lo
    
    cube = STRUCT([
        T([1,2,3])(lo),
        S([1,2,3])(cube_dim),
        CUBE(1)])
    
    stair = T([1,2,3])(lo)(
        fit_model_into_box(MAP([S1, S3, S2])(w3.genRun2(11)), *cube_dim))
    return stair, cube
    
    
def gen_level(
    root_path,
    floor_file = 'floor.lines',
    walls_file = 'walls.lines',
    windows_file = 'windows.lines',
    doors_file = 'doors.lines',
    handrails_file = 'handrails.lines',
    stairs_file = 'stairs.lines'):
    """
    Generates a level from the directory tree pointed by given path
    """
    
    def internal(
        floor_thickness = .3,
        walls_thickness = .2, 
        walls_height = 3, 
        windows_fn = default_window(),
        doors_fn = default_door(),
        doors_height = 2.3,
        handrails_height = 1.2,
        handrails_thickness = .1):
        
        floor = gen_floor(root_path + floor_file, floor_thickness)
        
        walls = w8.gen_walls(
            root_path + walls_file, 
            walls_thickness, 
            walls_height + floor_thickness, 
            external = False)
            
        windows = gen_windows(
            root_path + windows_file, 
            windows_fn,
            walls_height + floor_thickness)
            
        doors, doorways = gen_doors(
            root_path + doors_file, 
            doors_fn, 
            doors_height)
            
        handrails = w8.gen_walls(
            root_path + handrails_file, 
            handrails_thickness, 
            handrails_height + floor_thickness,
            external = False)
        
        stair_foot = gen_stairs_foot(root_path + stairs_file)
        walls = DIFFERENCE([walls, T(3)(floor_thickness)(doorways)])
        
        return walls, windows, doors, handrails, floor, stair_foot
            
    return internal
    
    
def gen_module(root_path, walls_height=3, floor_thickness=.3):
    """
    Generates a multi-storey module from the folder hierarchy
    pointed by root_path. Returns an HPC
    """
    levels = [gen_level(root_path + lv.rstrip() + '/')(
            floor_thickness = floor_thickness,
            walls_height = walls_height)
        for lv in os.popen('ls ' + root_path)]
    
    walls_hpc = []
    windows_hpc = []
    doors_hpc = []
    handrails_hpc = []
    floors_hpc = []
    stairs_foots = []
    lv = 0
    for walls, windows, doors, handrails, floor, stair_foot in levels:
        level_height = walls_height * lv
        
        walls_hpc.append(T(3)(level_height)(walls))
        windows_hpc.append(T(3)(level_height)(windows))
        doors_hpc.append(T(3)(level_height + floor_thickness)(doors))
        handrails_hpc.append(T(3)(level_height)(handrails))
        floors_hpc.append(T(3)(level_height)(floor))
        
        stairs_foots.append(stair_foot+[level_height])
        
        lv += 1
        
    walls_hpc = UNION(walls_hpc)
    windows_hpc = UNION(windows_hpc)
    doors_hpc = STRUCT(doors_hpc)
    handrails_hpc = UNION(handrails_hpc)
    floors_hpc = UNION(floors_hpc)
    
    cubes_hpc = []
    stairs_hpc = []
    for i in range(0, len(stairs_foots), 2):
        stair, cube = gen_stairs(stairs_foots[i], stairs_foots[i+1])
        cubes_hpc.append(cube)
        stairs_hpc.append(T(3)(floor_thickness)(stair))
    
    stairs_hpc = STRUCT(stairs_hpc)
    
    cubes_hpc = T(3)(floor_thickness)(STRUCT(cubes_hpc))
    floors_hpc = DIFFERENCE([floors_hpc, cubes_hpc])
    
    return STRUCT([
        walls_hpc,
        windows_hpc,
        doors_hpc,
        handrails_hpc,
        floors_hpc,
        stairs_hpc])
    

def default_door():
    """
    Returns a function to generate the default door.
    The default door is simply a frame.
    """
    X = [0.0, 0.14, 1.12, 1.26]
    Y = [0.0, 0.14, 2.24]
    Z = [-0.14, 0.14]
    V, F = True, False
    occupancy = [
        [[V], [V]],
        [[V], [F]],
        [[V], [V]]
    ]
    return w7.window(X, Y, Z, occupancy)
    
    
def default_window():
    """
    Returns a function to generate the default window.
    The default window is a basic four panels window.
    """
    X = [0, .125, 1.4375, 1.5625, 2.9375, 3.0625, 4.4375, 4.5625, 5.875, 6.0]
    Y = [0, .125, 2.875, 3.0]
    Z = [0, .125]
    V, F = True, False
    occupancy = [
        [[V],[V],[V]],
        [[V],[F],[V]],
        [[V],[V],[V]],
        [[V],[F],[V]],
        [[V],[V],[V]],
        [[V],[F],[V]],
        [[V],[V],[V]],
        [[V],[F],[V]],
        [[V],[V],[V]]
    ]
    return w7.window(X, Y, Z, occupancy)
    
    
if __name__=='__main__':
    path = './data/module1/'
    VIEW(gen_module(path))
    
