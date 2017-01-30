
# Final Workshop
# Reference: https://www.google.it/maps/@37.8149362,-122.235095,18z

from pyplasm import *
from workshop_10 import gen_module

def hermite(p1,p2,t1,t2):
    """
    Generates an hermite curve with two points and two vectors
    """
    h1 = lambda u: 2*u**3 -3*u**2 + 1
    h2 = lambda u: -2*u**3 + 3*u**2
    h3 = lambda u: u**3 -2*u**2 + u
    h4 = lambda u: u**3 - u**2
    def hermite0(p):
        u = p[0]
        basis = [h1(u),h2(u),h3(u),h4(u)]
        handles = TRANS([p1,p2,t1,t2])
        out = AA(INNERPROD)(DISTL([basis,handles]))
        return out
    return hermite0
    

def surface(x_div, y_div):
    """
    Returns an function that generates and hpc of a sampled curve 
    returned by a passed a function
    """
    ifn = INTERVALS
    return lambda f1, f2: \
        MAP(BEZIER(S2)([f1,f2]))(PROD([ifn(1)(x_div),ifn(1)(y_div)]))


def arimo_ave():
    upperFn = [
        hermite([96,431,0], [429,308,0], [150,-350,0], [400,-50,0]),
        hermite([429,308,0], [883,478,0], [400,-50,0], [0,400,0])]
    lowerFn = [
        hermite([111,435,0], [429,324,0], [200,-350,0], [400,-50,0]),
        hermite([429,324,0], [865,474,0], [400,-50,0], [100,400,0])]   
    return STRUCT(map(surface(20,1),upperFn,lowerFn))


def walavista_ave():
    upperFn = [
        hermite([0,397,0], [350,500,0], [347,101,0], [403,42,0]),
        hermite([350,500,0], [821,457,0], [403,42,0], [307,85,0]),
        hermite([821,457,0], [983,503,0], [307,85,0], [307,85,0])]
    lowerFn = [
        hermite([0,421,0], [350,514,0], [347,101,0], [403,42,0]),
        hermite([350,514,0], [821,474,0], [403,42,0], [307,85,0]),
        hermite([821,474,0], [983,517,0], [307,85,0], [307,85,0])]
    return STRUCT(map(surface(20,1),upperFn,lowerFn))
    
    
def block_arimo_walavista():
    mod1 = gen_module('./data/module1/')
    mod2 = gen_module('./data/module2/')
    modUnion = STRUCT([
        mod1,
        S(1)(-1),
        T([1,3])([-40,3]),
        mod2
    ])
    level = STRUCT([
        modUnion,
        T(2)(6),
        modUnion,
        T(2)(6),
        T(1)(40)(S(1)(-1)(modUnion)),
        T(2)(6),
        T(1)(40)(S(1)(-1)(modUnion)),
        T(2)(6),
        modUnion,
        T(2)(6),
        modUnion
    ])
    block = STRUCT([
        T(3)(18.3)(CUBOID([40,48,1])),
        CUBOID([40,6,18.3]),
        T(2)(6),
        level,
        T(3)(9.3)(level),
        T(2)(36),
        CUBOID([40,1,18.3])
    ])
    
    return STRUCT([
        T([1,2])([319,355]),
        R([1,2])(1.5),
        S([1,2,3])([3,-3,3]),
        block
    ])
    

if __name__=='__main__':
    
    model = STRUCT([
        #arimo_ave(),
        #walavista_ave(),
        block_arimo_walavista()
    ])
    VIEW(S(2)(-1)(model))
