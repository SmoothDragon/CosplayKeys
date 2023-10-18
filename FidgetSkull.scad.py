#!/usr/bin/env python

'''Nested fidget star with a twist
Uses svgSCAD package.
'''

import solid as sd
import numpy as np
import svgSCAD as svg
import itertools
from solid import *
from solid.utils import *


def koch_snowflake(R, pieces=6, iterations=3):
    scale = 1/3
    base = svg.hexagram(R)
    for _ in range(iterations):
        base2 = sd.scale(scale)(base)
        base3 = sd.translate([(1-scale)*R,0])(base2)
        base += sd.union()(*[sd.rotate([0,0,i*360/pieces])(base3) for i in range(pieces)])
    base = sd.rotate([0,0,30])(base)
    return base

def perimeter(shape, r, segments=6):
    border = sd.circle(r=r, segments=segments)
    final = sd.minkowski()(shape, border)
    final -= shape
    return final

def ring(R, r, height, twist, slices, scale, full=False):
    shape = skull_outline(R)
    if not full:
        shape = perimeter(shape, r, segments=50)
    graphic = sd.linear_extrude(height=10, twist=0, slices=slices, scale=scale)(shape)
    graphic += sd.rotate([0,180,0])(graphic)
    return graphic

def skull(R):
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
    return final

def skull_outline(R):
    head = sd.circle(R)
    lower = sd.scale([1,1.5])(head)
    head = sd.intersection()(head, svg.halfPlane('N'))
    lower = sd.intersection()(lower, svg.halfPlane('S'))
    head += lower
    return head


if __name__ == '__main__':
    R = 62
    fn = 100
    twist = 15
    slices=50
    scale=.8
    gap = 6
    gaps = [8,7.5,7,6.5,6,5.5]
    drops = list(itertools.accumulate(gaps, initial=0))

    final = sd.union()(*[ring(R-drop, 1.2, height=10, twist=twist, slices=slices, scale=scale) for drop in drops])
    R2 = R-drops[-1]-4
    inner_skull = sd.intersection()(
        ring(R2, 1.2, height=10, twist=twist, slices=slices, scale=scale, full=True),
        sd.linear_extrude(height=30, center=True)(skull(R2))
        )
    final += inner_skull
    final = sd.scad_render(final, file_header=f'$fn={fn};')
    print(final)


