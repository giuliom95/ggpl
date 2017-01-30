from pyplasm import *
import random as r

def gen_windows(plan_grid, n, m, window_model):
    return STRUCT([
        T([1,2])([j,i])(
            gen_cube_windows(plan_grid, window_model)(i, j, n, m))
        for i in range(n) 
        for j in range(m) 
        if plan_grid[i][j]])

def gen_cube_windows(plan_grid, window_model):
    w = window_model
    hpcs = [CUBE(0.00001)]
    
    def gen_cube0(i, j, n, m):
        if j+1 == m or not plan_grid[i][j+1]:
            hpcs.append(T([1, 2])([1, .5])(MAP([S2, S1, S3])(w)))
            
        if j-1 < 0 or not plan_grid[i][j-1]:
            hpcs.append(T(2)(.5)(MAP([S2, S1, S3])(w)))
            
        if i+1 == n or not plan_grid[i+1][j]:
            hpcs.append(T([1, 2])([.5, 1])(w))
            
        if i-1 < 0 or not plan_grid[i-1][j]:
            hpcs.append(T(1)(.5)(w))
        
        return STRUCT(hpcs)
    
    return gen_cube0
    

def gen_body(plan_grid, n, m):
    c = CUBE(1)
    return STRUCT([
        T([1,2])([j,i])(c)
        for i in range(n) 
        for j in range(m) 
        if plan_grid[i][j]])


def gen_house(
    box,
    plan_grid,
    door_model,
    window_model,
    roof_model):
    
    n = len(plan_grid)
    m = len(plan_grid[0])
    
    body = STRUCT([
        gen_body(plan_grid, n, m),
        T(3)(1),
        roof_model])
    
    l2s_scale = map(lambda x,y: x/y, SIZE([1,2,3])(body), box)
    s2l_scale = [1/elem for elem in l2s_scale]
    
    scaled_win = S([1,2,3])(l2s_scale)(window_model)
    
    windows = gen_windows(plan_grid, n, m, scaled_win)
    
    house = STRUCT([body, windows])
    
    return TEXTURE(['wood.jpg',True, True, 300,300, r.random()*3.1415, .1,.1, 0,0])(
        S([1,2,3])(s2l_scale)(house))


def l_shaped_house(box):
    
    grid = [
        [False, False, True],
        [True, True, True]]
    
    roof = MKPOL([
        [
            [  2,   0,  0],
            [2.5,   0, .5],
            [  3,   0,  0],
            [  3,   2,  0],
            [  0,   2,  0],
            [  0, 1.5, .5],
            [  0,   1,  0],
            [  2,   1,  0],
            [2.5, 1.5, .5]
        ],
        [
            [3,2,1],
            [9,2,3,4],
            [5,6,9,4],
            [7,6,5],
            [7,8,9,6],
            [9,8,1,2]
        ],
        [1]])
    
    window = T([1,2,3])([-.75, -.1, 1.2])(CUBOID([1.5, .2, 2]))
    return gen_house(box, grid, None, window, roof)
    
def q_shaped_house(box):

    grid = [
        [True, True, True],
        [True, True, True],
        [True, False, False]]
    roof = MKPOL([
        [
            [0,0,0], #1
            [3,0,0], #2
            [3,2,0], #3
            [1,2,0], #4
            [1,3,0], #5
            [.5,3,.5], #6
            [0,3,0], #7
            [.5,.5,.5], #8
            [2.5,.5,.5], #9
            [2.5,1.5,.5], #10
            [.5,1.5,.5] #11
        ],
        [
            [1,8,6,7],
            [1,2,9,8],
            [2,3,10,9],
            [10,3,4,11],
            [4,5,6,11],
            [6,5,7],
            [8,9,10,11]
        ],
        [1]])
    
    window = T([1,2,3])([-.75, -.1, 1.2])(CUBOID([1.5, .2, 2]))
    return gen_house(box, grid, None, window, roof)


def rectangular_house(box):

    grid = [
        [True, True],
        [True, True],
        [True, True]]
    roof = MKPOL([
        [
            [0,0,0], #1
            [1,0,1], #2
            [2,0,0], #3
            [2,3,0], #4
            [1,3,1], #5
            [0,3,0] #6
        ],
        [
            [1,2,5,6],
            [2,3,4,5],
            [1,3,2],
            [5,4,6]
        ],
        [1]])
    
    window = T([1,2,3])([-.75, -.1, 1.2])(CUBOID([1.5, .2, 2]))
    return gen_house(box, grid, None, window, roof)


def squared_house(box):
    
    grid = [
        [True, True, True],
        [True, True, True],
        [True, True, True]]
    roof = MKPOL([
        [
            [0,0,0], #1
            [3,0,0], #2
            [3,3,0], #3
            [0,3,0], #4
            [1.5,1.5,1] #5
        ],
        [
            [5,1,2],
            [5,2,3],
            [5,3,4],
            [5,4,1]
        ],
        [1]])
    
    window = T([1,2,3])([-.75, -.1, 1.2])(CUBOID([1.5, .2, 2]))
    return gen_house(box, grid, None, window, roof)
    

if __name__=='__main__':
    VIEW(squared_house([15, 15, 8]))

