#!/usr/bin/env python3

from solid import *
from solid.utils import *

from math import atan, sqrt


def parseArguments():
    # Argument parsing
    import argparse
    parser = argparse.ArgumentParser(
        description='Generate SCAD for half Sierpinski cube.')
    parser.add_argument('-n', action='store', default='20', dest='iterations',
        type=int, help='Number or iterations to apply.')
    parser.add_argument('--size', action='store', default='81', dest='size',
        type=float, help='Side length (in millimeters) of cube.')
    parser.add_argument('--twist', action='store', default=22.5, dest='twist',
        type=float,)
    parser.add_argument('--shift', action='store', default=10, dest='shift',
        type=float,)
    parser.add_argument('--scale', action='store', default=.9, dest='scale_xyz',
        type=float,)
    return parser.parse_args()


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

def triforce(base=6):
    '''Height will be base*sqrt(3)/3
    '''
    bs3 = base*sqrt(3)
    points = [ (-base/2, -bs3/6, 0), (base/2, -bs3/6, 0), (0, base*sqrt(3)/2-bs3/6, 0), (0, 0, base*sqrt(3)/6) ]
    faces = [
        [0,1,2],
        [0,3,1],
        [0,2,3],
        [1,3,2],
        ]
    pyramid = polyhedron(points=points, faces=faces)
    pyramid = translate([0, .4*base, 0])(pyramid)
    tri_pyramid = pyramid + rotate([0,0,120])(pyramid) + rotate([0,0,240])(pyramid)
    tri_pyramid = intersection()(tri_pyramid, cube([2*base, 2*base, base*sqrt(3)/6], center=True))
    tri_pyramid += mirror([0,0,1])(tri_pyramid)
    tri_pyramid = translate([0,0,base*sqrt(3)/12])(tri_pyramid)
    return tri_pyramid


def make_key(bow_width=25, bow_bevel=1.2, bow_hole_width=20, bow_fn=128, 
             shaft_length=50, shaft_width=3.6, shaft_base=1.2, 
             small_bit_length=8, large_bit_length=12,
             tooth_width=5,
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

    bow = cylinder(d=bow_width, h=shaft_width, segments=bow_fn)
    cut_base = bow_width + (2*shaft_width - bow_bevel)
    cut_bow_bevel = cylinder(d1=cut_base, d2=0, h=cut_base/2)
    bow = intersection()(bow, cut_bow_bevel)
    bow = translate([0,0,shaft_width])(rotate([180,0,0])(bow))
    bow = intersection()(bow, cut_bow_bevel)

    tooth = linear_extrude(height=.5*tooth_width, center=True, scale=.3)(square([.5*tooth_width, tooth_width], center=True))
    tooth = rotate([0,-90,0])(tooth)
    tooth = translate([-.5*(bow_width+.2*tooth_width),0,shaft_width/2])(tooth)

    bow_hole = translate([0,0,-shaft_width])(cylinder(d=bow_hole_width, h=3*shaft_width, segments=bow_fn))

    final = bow + shank - bow_hole + rotate([0,0,90])(triforce(shaft_width*6/sqrt(3)))
    for i in range(8):
        final += rotate([0,0,i*45])(tooth)
    return final


if __name__ == '__main__':
    args = parseArguments()

    final = beveled_box(length=60, diameter=10, base=2)
    final = make_key()
    # final = triforce()
    print(scad_render(final))
