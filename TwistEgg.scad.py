#!/usr/bin/env python

'''Twisting egg
'''

import solid2 as sd
import svgSCAD as d2
# import solid2.extensions.bosl2 as bosl

def cutter(middle):
    blade = d2.sector(45)
    blade = sd.rotate(-22.5)(blade)
    blade = sd.translate([.2,0])(blade)
    blade &= sd.circle(50)
    blade = sd.union()(*[sd.rotate(90*i)(blade) for i in range(4)])
    return sd.linear_extrude(height=middle, twist=90, center=True)(blade)

if __name__ == '__main__':
    # fn = 256
    fn = 64
    ridge = 4
    tip = .4

    r = 30
    wall=4
    middle = 50

    # CHOOSE one of the following:
    final = d2.egg(r)-d2.egg(r-wall)
    final &= d2.halfPlane('R')
    final = sd.rotate_extrude()(final)
    final = sd.translate([0,0,-5])(final)
    top = final & sd.translate([0,0,middle])(sd.cube([1000,1000,middle], center=True))
    bottom = final & sd.translate([0,0,-middle])(sd.cube([1000,1000,middle], center=True))
    swirl = final & cutter(middle)
    top = swirl + top
    bottom += sd.rotate([0,0,45])(swirl)
    final = top
    # final = bottom


    # final = bosl.egg(r1=5, r2=10, R=30, length=20)
    # final = puzzle_box_lid()

    # This was just to see how they lined up.
    # lid = puzzle_box_lid()
    # lid = sd.mirror([0,0,1])(lid)
    # lid = sd.translate([0,0,50+2*ridge-2*tip+4.4])(lid)
    # final += lid
    final = sd.scad_render(final, file_header=f'$fn={fn};')
    print(final)


