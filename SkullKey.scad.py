#!/usr/bin/env python

'''Challenge coin for cutting and etching on a laser cutter.
Uses svgSCAD package.
'''

import solid as sd
import numpy as np
import svgSCAD as svg
from solid import *
from solid.utils import *


def beveled_square(diameter, base, center=True):
    '''Each corner of the square is beveled at a 45 degree angle
    diameter: side to side distance of octagon
    base: length of bottom rectilinear flat side 0 < base < diameter
    base == 0 => square diamond
    base == diameter => square
    '''
    # TODO: make points from parameters
    x = diameter/2
    y = base/2
    points = [ (x,y), (y,x), (-y,x), (-x,y), (-x,-y), (-y,-x), (y,-x), (x,-y) ]
    shape = polygon(points=points)
    return shape

def beveled_box(length, diameter, base, beveled_end=True, center=False):
    '''Octogon shaped segment
    Ends are cut so that two rods can be joined at 90 degrees
    length: X-direction
    diameter: Y-direction
    diameter: Z-direction
    Will be placed in the same location as cube([X,Y,Z])
    center: Positions beveled_box with respect to origin identically to cube()
    '''
    shape = beveled_square(diameter=diameter, base=base)
    rod = linear_extrude(height=length, center=True, convexity=10, twist=0)(shape)
    if beveled_end:
        cut_length = (length + base)/sqrt(2)
        cut_block = rotate([45,0,0])(cube(cut_length, center=True))
        rod = intersection()(rod, cut_block, rotate([0,0,90])(cut_block))
    final = rotate([0,90,0])(rod)  # lay in XY plane
    if not center:
        final = translate([length/2, diameter/2, diameter/2])(final)
    return final


def make_key(bow_width=25, bow_bevel=1.2, bow_hole_width=12.5, bow_fn=128, 
             shaft_length=50, shaft_width=6, shaft_base=1.2, 
             small_bit_length=13, large_bit_length=18,
             tooth_width=6,
             ):
    shaft = beveled_box(length=shaft_length, diameter=shaft_width, base=shaft_base)

    small_bit = beveled_box(length=small_bit_length, diameter=shaft_width, base=shaft_base)
    small_bit = rotate([0,0,90])(small_bit)
    small_bit = translate([shaft_length - 0.5*shaft_width, 0, 0])(small_bit)

    large_bit = beveled_box(length=large_bit_length, diameter=shaft_width, base=shaft_base)
    large_bit = rotate([0,0,90])(large_bit)
    large_bit = translate([shaft_length - 2*shaft_width, 0, 0])(large_bit)

    collar = beveled_box(length=2, diameter=shaft_width, base=3*shaft_base, beveled_end=False)
    collar = translate([0,-shaft_base/2,0])(collar) + translate([0,shaft_base/2,0])(collar)
    collar1 = translate([20,0,0])(collar)
    collar2 = translate([15,0,0])(collar)

    shank = union()(shaft, small_bit, large_bit, collar1, collar2)
    shank = translate([0,-shaft_width/2,0])(shank)
    return shank

    bow = cylinder(d=bow_width, h=shaft_width, segments=bow_fn)
    cut_base = bow_width + (2*shaft_width - bow_bevel)
    cut_bow_bevel = cylinder(d1=cut_base, d2=0, h=cut_base/2)
    bow = intersection()(bow, cut_bow_bevel)
    bow = translate([0,0,shaft_width])(rotate([180,0,0])(bow))
    bow = intersection()(bow, cut_bow_bevel)

    tooth = linear_extrude(height=.9*tooth_width, center=True, scale=[.3,.5])(square([.95*tooth_width, .75*tooth_width], center=True))
    tooth = rotate([0,-90,0])(tooth)
    tooth = translate([-.5*(bow_width+.2*tooth_width),0,shaft_width/2])(tooth)

    bow_hole = translate([0,0,-shaft_width])(cylinder(d=bow_hole_width, h=3*shaft_width, segments=8))

    final = bow + shank - bow_hole

    holed_tooth = linear_extrude(height=1*tooth_width, center=True, scale=[.5,.8])(square([.85*tooth_width, 1.5*tooth_width], center=True))
    holed_tooth -= linear_extrude(height=.5*tooth_width, center=True, scale=.8)(square([1.75*tooth_width, .9*tooth_width], center=True))

    holed_tooth = rotate([0,-90,0])(holed_tooth)
    holed_tooth = translate([-.5*(bow_width+.2*tooth_width),0,shaft_width/2])(holed_tooth)
    final += (holed_tooth)
    for i in range(1,8):
        if i == 4:
            continue  # skip the ooth on the shank
        final += rotate([0,0,i*45])(tooth)
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

    inner_head = sd.scale(.95*.3)(head)
    frame = sd.linear_extrude(6,center=True)(inner_head) \
            + sd.linear_extrude(4,center=True)(sd.scale(.3)(head))
    frame = sd.translate([0,0,3])(frame)
    frame = sd.hull()(frame)
    frame = sd.rotate([0,0,90])(frame)
    final = sd.scale(.3)(final)
    final = sd.rotate([0,0,90])(final)
    final = sd.linear_extrude(6)(final)
    final = sd.intersection()(final, frame)
    final += sd.translate([17,0,0])(make_key())
    final = sd.scale(1.5)(final)

    print(sd.scad_render(final, file_header=f'$fn={fn};'))

    # print(svg.scadSVG(final, fn=fn, fill='blue')) #+svg.scadSVG(image2, fn=fn, fill='lightgreen'))




