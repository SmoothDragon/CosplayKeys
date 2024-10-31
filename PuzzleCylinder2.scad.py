#!/usr/bin/env python

'''Inspired by Hex Flex puzzle box, winner of 2023 puzzle of the year.
Both the lid and the base are supposed to be printed in Vase mode.
It may make sense to hide the cut with some number of lines on the bottom and top.

TODO:
If lines are added added to the sides, then the spiralize mode would need to be adjusted.
'''

import solid2 as sd

def puzzle_box_base(tip=.6, h_base = 1.2):
    gap = .1
    d_puzz = 100
    h_puzz = 25
    ridge = 4
    epsilon = 0.01
    MAX = 1000

    final = sd.cylinder(d=d_puzz, h=h_puzz)
    # Remove central cylinder
    final -= sd.translate([0,0,h_base])(sd.cylinder(d=d_puzz-4*tip, h=h_puzz))
    # final -= sd.translate([0,MAX/2-(d_puzz-4*tip)/2,0])(sd.cube([gap,MAX,MAX], center=True))
    final -= sd.translate([0,MAX/2,0])(sd.cube([gap,MAX,MAX], center=True))
    top = sd.cylinder(d1=d_puzz, d2=d_puzz-2*ridge-2*gap, h=ridge)
    top -= sd.translate([0,0,-epsilon])(sd.cylinder(d1=d_puzz-4*tip, d2=d_puzz-2*ridge-2*gap-4*tip, h=ridge+2*epsilon))
    top2 = sd.cylinder(d1=d_puzz-2*ridge-2*gap, d2=d_puzz-4*tip-2*gap, h=ridge-2*tip)
    top2 -= sd.translate([0,0,-epsilon])(sd.cylinder(d1=d_puzz-2*ridge-2*gap-4*tip, d2=d_puzz-2*gap-8*tip, h=ridge-2*tip+2*epsilon))
    cutline = sd.cube([gap, MAX, .8], center=True)
    final -= sd.union()(*[sd.rotate([0,0,i*360/8])(cutline) for i in range(8)])
    vertbump = sd.cube([1+2*tip, gap+4*tip, h_puzz])
    vertbump = sd.translate([d_puzz/2-1-2*tip,-(gap+4*tip)/2,0])(vertbump)
    vertbumps = sd.union()(*[sd.rotate([0,0,i*360/8])(vertbump) for i in range(8)])
    final += vertbumps
    vertline = sd.cube([2, gap, MAX], center=True)
    vertline = sd.translate([d_puzz/2,0,0])(vertline)
    final -= sd.union()(*[sd.rotate([0,0,i*360/8])(vertline) for i in range(8)])
    final += sd.translate([0,0,h_puzz])(top)
    top = sd.cylinder(d1=d_puzz, d2=d_puzz-2*ridge-2*gap, h=ridge)
    final += sd.translate([0,0,h_puzz])(top & vertbumps)
    vertline = sd.translate([0,0, 4*tip])(vertline)
    final -= sd.union()(*[sd.rotate([0,0,i*360/8])(vertline) for i in range(8)])
    final += sd.translate([0,0,h_puzz+ridge])(top2)
    final -= sd.translate([0,MAX/2,0])(sd.cube([gap,MAX,MAX], center=True))
    # final -= sd.translate([0,MAX/2-d_puzz/2+3*tip,0])(sd.cube([gap,MAX,MAX], center=True))
    # final -= sd.translate([0,MAX/2-d_puzz/2+3*tip,-MAX/2+h_base+gap])(sd.cube([gap,MAX,MAX], center=True))
    final -= sd.translate([0,MAX/2,-MAX/2+h_base+gap])(sd.cube([gap,MAX,MAX], center=True))
    return final

def puzzle_box_lid(tip, h_base):
    gap = .1
    d_puzz = 100
    h_puzz = 5
    ridge = 4
    epsilon = 0.01
    MAX = 1000

    final = sd.cylinder(d=d_puzz, h=h_puzz)
    final -= sd.translate([0,0, h_base])(sd.cylinder(d=d_puzz-4*tip, h=h_puzz))
    # final -= sd.translate([0,MAX/2-(d_puzz-4*tip)/2,0])(sd.cube([gap,MAX,MAX], center=True))
    final -= sd.translate([0,MAX/2,0])(sd.cube([gap,MAX,MAX], center=True))
    top = sd.cylinder(d=d_puzz, h=2*ridge-4*tip)
    top1 = sd.cylinder(d2=d_puzz-2*ridge, d1=d_puzz-4*tip, h=ridge-2*tip+epsilon)
    top2 = sd.cylinder(d1=d_puzz-2*ridge, d2=d_puzz-4*tip, h=ridge-2*tip+epsilon)
    top -= sd.translate([0,0,0])(top1)
    top -= sd.translate([0,0,ridge-2*tip])(top2)
    vertbump = sd.cube([1+tip, gap+4*tip, h_puzz+ridge])
    vertbump = sd.translate([d_puzz/2-1-tip,-(gap+4*tip)/2,0])(vertbump)
    vertbumps = sd.union()(*[sd.rotate([0,0,i*360/8])(vertbump) for i in range(8)])
    final += vertbumps
    vertline = sd.cube([1, gap, MAX], center=True)
    vertline = sd.translate([d_puzz/2,0,0])(vertline)
    final += sd.translate([0,0,h_puzz])(top)
    final -= sd.union()(*[sd.rotate([0,0,i*360/8])(vertline) for i in range(8)])
    final -= sd.translate([0,MAX/2,0])(sd.cube([gap,MAX,MAX], center=True))
    cutline = sd.cube([gap, MAX, .8], center=True)
    final -= sd.union()(*[sd.rotate([0,0,i*360/8])(cutline) for i in range(8)])
    return final


if __name__ == '__main__':
    fn = 512
    # fn = 64
    ridge = 4
    tip = .6
    h_base=1.2

    # CHOOSE one of the following:
    # final = puzzle_box_base(tip, h_base)
    final = puzzle_box_lid(tip, h_base)

    # This was just to see how they lined up.
    # lid = puzzle_box_lid()
    # lid = sd.mirror([0,0,1])(lid)
    # lid = sd.translate([0,0,50+2*ridge-2*tip+4.4])(lid)
    # final += lid
    final = sd.scad_render(final, file_header=f'$fn={fn};')
    print(final)


