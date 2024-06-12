#!/usr/bin/env python

'''Challenge coin for cutting and etching on a laser cutter.
Uses svgSCAD package.
'''

import solid2 as sd
import numpy as np
import svgSCAD as svg
# from solid import *
# from solid.utils import *


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
    shape = sd.polygon(points=points)
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
    rod = sd.linear_extrude(height=length, center=True, convexity=10, twist=0)(shape)
    if beveled_end:
        cut_length = (length + base)/np.sqrt(2)
        cut_block = sd.rotate([45,0,0])(sd.cube(cut_length, center=True))
        rod = sd.intersection()(rod, cut_block, sd.rotate([0,0,90])(cut_block))
    final = sd.rotate([0,90,0])(rod)  # lay in XY plane
    if not center:
        final = sd.translate([length/2, diameter/2, diameter/2])(final)
    return final


def make_key(bow_width=25, bow_bevel=1.2, bow_hole_width=12.5, bow_fn=128, 
             shaft_length=50, shaft_width=6, shaft_base=1.2, 
             small_bit_length=13, large_bit_length=18,
             tooth_width=6,
             ):
    shaft = beveled_box(length=shaft_length, diameter=shaft_width, base=shaft_base)

    small_bit = beveled_box(length=small_bit_length, diameter=shaft_width, base=shaft_base)
    small_bit = sd.rotate([0,0,90])(small_bit)
    small_bit = sd.translate([shaft_length - 0.5*shaft_width, 0, 0])(small_bit)

    large_bit = beveled_box(length=large_bit_length, diameter=shaft_width, base=shaft_base)
    large_bit = sd.rotate([0,0,90])(large_bit)
    large_bit = sd.translate([shaft_length - 2*shaft_width, 0, 0])(large_bit)

    collar = beveled_box(length=2, diameter=shaft_width, base=3*shaft_base, beveled_end=False)
    collar = sd.translate([0,-shaft_base/2,0])(collar) + sd.translate([0,shaft_base/2,0])(collar)
    collar1 = sd.translate([20,0,0])(collar)
    collar2 = sd.translate([15,0,0])(collar)

    shank = sd.union()(shaft, small_bit, large_bit, collar1, collar2)
    shank = sd.translate([0,-shaft_width/2,0])(shank)
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

def pathHeart(R, angle=45):
    L = 100
    r = 6
    base = 2
    octagon = beveled_square(r, base)
    bump = sd.rotate_extrude(180)(sd.translate([R,0])(octagon))
    side = beveled_box(2*L, r, base, beveled_end=False, center=True) 
    side = sd.rotate(90)(side)
    bump += sd.translate([-R,-L,0])(side)
    bump += sd.translate([R,-L,0])(side)
    bump = sd.translate([R,0,0])(bump)
    bump = sd.rotate([0,0,-angle])(bump)
    cutblock = sd.cube(1000, center=True)
    cutblock = sd.translate([500,0,0])(cutblock)
    half = sd.intersection()(bump, cutblock)
    heart = half + sd.mirror([1,0,0])(half)
    heart = sd.translate([0,0,-r/2])(heart)
    return heart



if __name__ == '__main__':
    fn = 512
    R = 10
    thickness = 6

    final = pathHeart(R, angle=30)
    final = sd.translate([3.8,3*R-4,3])(final)
    cutter = sd.cube(30)
    cutter = sd.translate([0,-10,0])(cutter)
    cutter = sd.rotate([0,-45,90])(cutter)
    final -= sd.translate([0,9,2.5])(cutter)
    final -= sd.translate([0,11.5,2.5])(cutter)
    cutter = sd.rotate([0,0,60])(cutter)
    final -= sd.translate([0,-5,2.5])(cutter)
    final -= sd.translate([0,-9.5,2.5])(cutter)

    cutter = sd.cube(50)
    cutter = sd.translate([0,-25,0])(cutter)
    cutter = sd.rotate([0,135,90])(cutter)
    final -= sd.translate([0,5,-2.5])(cutter)
    final -= sd.translate([0,2,-2.5])(cutter)
    final = sd.mirror([0,0,1])(final)
    # final -= sd.rotate([0,0,60])(sd.translate([0,9,2.5])(cutter))
    final += sd.rotate([0,0,120])(final)+ sd.rotate([0,0,240])(final)
    print(sd.scad_render(final, file_header=f'$fn={fn};'))

    # print(svg.scadSVG(final, fn=fn, fill='blue')) #+svg.scadSVG(image2, fn=fn, fill='lightgreen'))




