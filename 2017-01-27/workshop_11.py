
# Final Workshop

from pyplasm import *
import houses as h

PI = 3.141592654

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
    
def base():
    return TEXTURE(['wood.jpg',True,True, 0,0, PI/2, 1,1, 0,0 ]) \
        (S(3)(-1)(CUBOID([289,188,4])))

    
def houses():
    k = PI/180
    return STRUCT([
        T([1,2])([203,37])(R([1,2])(19*k)(h.q_shaped_house([21,28,8]))),
        T([1,2])([176,40])(R([1,2])(22*k)(h.squared_house([17,14,12]))),
        T([1,2])([132,36])(R([1,2])(-4*k)(h.squared_house([17,16,12]))),
        T([1,2])([78,40])(R([1,2])(-14*k)(h.rectangular_house([16.5,23,10]))),
        T([1,2])([47,54])(R([1,2])(-23.6*k)(h.squared_house([17,19,9]))),
        T([1,2])([15,26])(R([1,2])(-2*k)(h.rectangular_house([14,19,10]))),
        T([1,2])([25,137])(R([1,2])(-30*k)(h.squared_house([14,18,8]))),
        T([1,2])([42,126])(R([1,2])(-29*k)(h.squared_house([16,17,10]))),
        T([1,2])([81,136])(R([1,2])(-27*k)(S(2)(-1)(h.q_shaped_house([18,27,8])))),
        T([1,2])([106,121])(R([1,2])(-110*k)(h.rectangular_house([15,20,10]))),
        T([1,2])([151,98])(R([1,2])(82*k)(h.l_shaped_house([23,21.5,10]))),
        T([1,2])([178,127])(R([1,2])(197*k)(h.l_shaped_house([23,18,10]))),
        T([1,2])([159,148])(R([1,2])(-22*k)(h.squared_house([21,21,13]))),
        T([1,2])([194,140])(R([1,2])(-17*k)(h.squared_house([17,17,11]))),
        T([1,2])([255,130])(R([1,2])(-15*k)(S(2)(-1)(h.l_shaped_house([22,16,9])))),
        T([1,2])([238,104])(R([1,2])(-115*k)(h.rectangular_house([15,17,10]))),
        T([1,2])([253,136])(R([1,2])(-6*k)(h.rectangular_house([16,18,10]))),
        T([1,2])([271,82])(R([1,2])(117*k)(S(1)(-1)(h.q_shaped_house([17,23,8])))),
        T([1,2])([260,36])(R([1,2])(10*k)(h.rectangular_house([17,19,10]))),
        T([1,2])([15,72])(R([1,2])(-28*k)(h.rectangular_house([14,19,9])))
    ])
    

def roads():
    stephanie1 = hermite([0,123,0], [238,171,0], [194,-117,0], [46,520,0])
    stephanie2 = hermite([0,134,0], [229,171,0], [194,-104,0], [57,500,0])
    irondale1 = hermite([202, 92, 0], [230, 27, 0], [80,-82,0], [0,-50,0])
    irondale2 = hermite([209, 97, 0], [239, 27, 0], [80,-82,0], [0,-50,0])
    skouras1 = hermite([161, 188, 0], [289, 164, 0], [84, -37, 0], [88, 0, 0])
    skouras2 = hermite([189, 188, 0], [289, 173, 0], [75, -23, 0], [88, 0, 0])
    
    s = surface(30, 1)
    return TEXTURE('wood.jpg')(
        STRUCT([
            T(3)(.1),
            s(stephanie1, stephanie2),
            s(irondale1, irondale2),
            s(skouras1, skouras2),
            MKPOL([[[110,25],[119,25],[123,72],[114,72]], [[1,2,3,4]], [1]])
        ])
    )
    

if __name__=='__main__':
    
    model = STRUCT([
        houses(),
        base(),
        roads()
    ])
    VIEW(S(2)(-1)(model))