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

def bevel_shape(shape, scale, max_height, min_height):
    inner_shape = sd.scale(.95)(shape)
    frame = sd.linear_extrude(max_height,center=True)(inner_shape) \
            + sd.linear_extrude(min_height,center=True)(shape)
    frame = sd.hull()(frame)
    return frame

def wedge(R, angle, center=False):
    shape = sd.square(R)
    if angle<=90:
        shape = sd.intersection()(shape, sd.rotate([0,0,angle-90])(shape))
    else:
        shape = sd.union()(shape, sd.rotate([0,0,90-angle])(shape))
    if center:
        shape = sd.rotate([0,0,-angle/2])(shape)
    return shape

def heart2(R):
    shape = sd.circle(R)
    shape = sd.scale([2,1])(shape)
    shape = sd.rotate([0,0,45])(shape)
    shape = sd.intersection()(shape, svg.halfPlane('R'))
    shape += sd.mirror([1,0])(shape)
    return shape

def leminscate(R):
    shape = sd.circle(R)
    shape = sd.translate([np.sqrt(2)*R,0])(shape)
    corner = sd.square(R)
    corner = sd.rotate([0,0,-45])(corner)
    shape += corner
    shape += sd.mirror([1,0])(shape)
    return shape

def heart(R):
    curve = sd.circle(d=R)
    shape = sd.translate([R,R/2])(curve)
    shape += sd.translate([R/2,R])(curve)
    # shape += sd.rotate([0,0,90])(shape)
    shape += sd.square(R)
    shape = sd.rotate([0,0,45])(shape)
    # shape = sd.scale([2,1])(shape)
    # shape = sd.intersection()(shape, svg.halfPlane('R'))
    # shape += sd.mirror([1,0])(shape)
    return shape

if __name__ == '__main__':
    fn = 512
    R = 17
    thickness = 6

    head = sd.circle(R)
    head = bevel_shape(head, scale=.95, max_height=thickness, min_height=.66*thickness)
    # lower = sd.scale([1,1.5])(head)
    # head = sd.intersection()(head, svg.halfPlane('N'))
    lower = sd.square(1.3*R,center=True)
    lower = bevel_shape(lower, scale=.95, max_height=thickness, min_height=.66*thickness)
    lower = sd.translate([0,-.8*R, 0])(lower)
    head += lower
    head = sd.translate([0,0,thickness/2])(head)

    eye = sd.circle(R/4)
    eye += sd.union()(*[sd.rotate([0,0,30*i])(sd.scale([1,.6])(leminscate(R/8))) for i in range(12)])
    # eye += sd.union()(*[sd.rotate([0,0,30*i])(sd.square([1.2*R/2, R/30], center=True)) for i in range(12)])
    eye = sd.translate([R/2,0,0])(eye)
    eye += sd.mirror([1,0])(eye)

    nose = heart(.2*R)
    nose = sd.rotate([0,0,180])(nose)
    nose = sd.translate([0,-.2*R])(nose)
    nose = heart2(.2*R)
    nose = sd.rotate([0,0,180])(nose)
    nose = sd.scale([.5,.8])(nose)
    nose = sd.translate([0,-.3*R])(nose)
    # nose += sd.mirror([0,1])(nose)

    headpiece = leminscate(R/8)
    headpiece = sd.scale([1,.4])(headpiece)
    headpiece = sd.intersection()(headpiece, svg.halfPlane('R'))
    headpiece = sd.translate([.12*R,0])(headpiece)
    headpiece = sd.union()(*[sd.rotate([0,0,30*i])(headpiece) for i in range(7)])
    headpiece += sd.circle(R*.09)
    headpiece = sd.translate([0,.45*R])(headpiece)

    smile = sd.circle(1.09*R)
    smile -= sd.scale(.93)(smile)
    smile = sd.intersection()(smile, wedge(2*R, 50, center=True))
    smile = sd.rotate([0,0,-90])(smile)

    toothgap = sd.square([R*.09, .25*R], center=True)
    toothgap = sd.translate([0,-1.04*R])(toothgap)
    toothgap = sd.union()(*[sd.rotate([0,0,20/2*i])(toothgap) for i in range(-2,3)])
    smile += toothgap
    # toothgap += sd.circle(d=R/30)
    # teethgap = sd.union()(*[sd.translate([(i-1)*13, -30])(toothgap) for i in range(3)])
    # toothcap = sd.hull()(toothgap, sd.translate([0,-10*R])(toothgap))
    cutout = eye + nose + smile + headpiece
    cutout = sd.linear_extrude(30)(cutout)
    cutout = sd.translate([0,0,-10])(cutout)
    final = head - cutout
            # - cheek - sd.mirror([1,0])(cheek)\
            # - teethgap\
            # - eye - sd.mirror([1,0])(eye)
    # print(sd.scad_render(final, file_header=f'$fn={fn};'))

    # inner_head = sd.scale(.95*.3)(head)
    # frame = sd.linear_extrude(6,center=True)(inner_head) \
            # + sd.linear_extrude(4,center=True)(sd.scale(.3)(head))
    # frame = sd.translate([0,0,3])(frame)
    # frame = sd.hull()(frame)
    # frame = sd.rotate([0,0,90])(frame)
    # final = sd.scale(.3)(final)
    # final = sd.rotate([0,0,90])(final)
    # final = sd.linear_extrude(6)(final)
    # final = sd.intersection()(final, frame)
    # final = sd.rotate([0,0,90])(final)
    final += sd.rotate([0,0,-90])(sd.translate([17,0,0])(make_key()))
    final -= cutout
    final = sd.scale(1.5)(final)

    print(sd.scad_render(final, file_header=f'$fn={fn};'))

    # print(svg.scadSVG(final, fn=fn, fill='blue')) #+svg.scadSVG(image2, fn=fn, fill='lightgreen'))




