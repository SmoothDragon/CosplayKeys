#!/usr/bin/env python

'''Challenge coin for cutting and etching on a laser cutter.
Uses svgSCAD package.
'''

import solid as sd
import numpy as np
import svgSCAD as svg

def pentagram(R):
    wedge = sd.square(R)
    wedge = sd.intersection()(
                sd.rotate([0,0,18])(wedge),
                sd.rotate([0,0,72])(wedge),
                sd.translate([-R/2,0])(wedge),
                )
    wedge = sd.translate([0,-R])(wedge)
    wedge = sd.rotate([0,0,180])(wedge)
    base = sd.union()(*[sd.rotate([0,0,i*360/pieces])(wedge) for i in range(pieces)])

def starfish(R, pieces=5, iterations=3):
    scale = 1-1/phi
    wedge = sd.square(R)
    wedge = sd.intersection()(
                sd.rotate([0,0,18])(wedge),
                sd.rotate([0,0,72])(wedge),
                sd.translate([-R/2,0])(wedge),
                )
    wedge = sd.translate([0,-R])(wedge)
    wedge = sd.rotate([0,0,180])(wedge)
    base = sd.union()(*[sd.rotate([0,0,i*360/pieces])(wedge) for i in range(pieces)])
    for _ in range(iterations):
        base2 = sd.scale(scale)(base)
        base3 = sd.translate([0,(1-scale)*R])(base2)
        base += sd.union()(*[sd.rotate([0,0,i*360/pieces])(base3) for i in range(pieces)])
    return base

def stack3(final, R):
    # Make 20 copies in square
    sy = 1.8
    sx = 1.5
    sY = 4.6
    final += sd.translate([0,sy*R])(final) + sd.translate([0,2*sy*R])(final)
    return final

if __name__ == '__main__':
    fn = 64
    R = 50

    head = sd.circle(R)
    lower = sd.scale([1,1.5])(head)
    head = sd.intersection()(head, svg.halfPlane('N'))
    lower = sd.intersection()(lower, svg.halfPlane('S'))
    head += lower
    eye = head
    eye = sd.scale([.25,.25])(eye)
    eye = sd.rotate([0,0,-90])(eye)
    eye = sd.intersection()(eye, svg.halfPlane('S'))
    nose = sd.scale([.125,.125])(head)
    eye = sd.translate([30,0])(eye)
    eye = sd.rotate([0,0,20])(eye)
    nose = sd.rotate([0,0,180])(nose)
    nose = sd.intersection()(nose, svg.halfPlane('R'))
    nose = sd.rotate([0,0,-20])(nose)
    nose = sd.translate([-7,-15])(nose)


    cheek = svg.sector(30, R/10)
    cheek = sd.rotate([0,0,-90])(cheek)
    cheek = sd.translate([R/2,0])(cheek)
    toothgap = sd.square([R/30,1000], center=True)
    toothgap = sd.translate([0,-500])(toothgap)
    toothgap += sd.circle(d=R/30)
    teethgap = sd.union()(*[sd.translate([(i-1)*13, -30])(toothgap) for i in range(3)])
    # toothcap = sd.hull()(toothgap, sd.translate([0,-10*R])(toothgap))
    
    final = head\
            - cheek - sd.mirror([1,0])(cheek)\
            - teethgap\
            - nose - sd.mirror([1,0])(nose)\
            - eye - sd.mirror([1,0])(eye)

    print(sd.scad_render(final, file_header=f'$fn={fn};'))

    # print(svg.scadSVG(final, fn=fn, fill='blue')) #+svg.scadSVG(image2, fn=fn, fill='lightgreen'))




