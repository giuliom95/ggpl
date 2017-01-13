import os
from pyplasm import *
import numpy as np
import workshop_09 as w9    # Roofs and math funcs
import workshop_08 as w8    # .lines files utilities
import workshop_07 as w7    # Windows

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
                MAP([S1, S3, S2]),
                T([1, 2])(p1),
                R([1, 3])(angle),
                fn(v_len, height, 1)
            ]))
    return STRUCT(hpcs)
    
    
def gen_level(
    root_path,
    floor_file = 'floor.lines',
    walls_file = 'walls.lines',
    windows_file = 'windows.lines'):
    """
    Generates a level from the directory tree pointed by given path
    """
    
    def internal(
        windows_fn = default_window(),
        wall_thickness = .2, 
        wall_height = 3, 
        floor_thickness = .3):
        
        floor = gen_floor(root_path + floor_file, floor_thickness)
        walls = w8.gen_walls(
            root_path + walls_file, 
            wall_thickness, 
            wall_height, 
            False)
        windows = gen_windows(
            root_path + windows_file, 
            windows_fn, 
            wall_height)
        
        return STRUCT([
            floor,
            walls,
            windows])
            
    return internal
    
    
def default_window():
    """
    Returns a function to generate the default window.
    The default window is a basic four panels window.
    """
    X = [0.0, 0.125, 1.4375, 1.5625, 2.9375, 3.0625, 4.4375, 4.5625, 5.875, 6.0]
    Y = [0.0, 0.125, 2.875, 3.0]
    Z = [0.0, 0.125]
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
    path = './data/module1/level1/'
    #VIEW(default_window()(6,3,.125))
    VIEW(gen_level(path)())
