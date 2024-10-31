#!/usr/bin/env python

'''Inspired by Hex Flex puzzle box, winner of 2023 puzzle of the year.
Both the lid and the base are supposed to be printed in Vase mode.
It may make sense to hide the cut with some number of lines on the bottom and top.

TODO:
If lines are added added to the sides, then the spiralize mode would need to be adjusted.
'''

import solid2 as sd

def puzzle_box_base():
    tip = 1
    gap = .1
    d_puzz = 100
    h_puzz = 50
    ridge = 4
    epsilon = 0.01
    MAX = 1000
    h_base = 2

    final = sd.cylinder(d=d_puzz, h=h_puzz)
    final -= sd.translate([0,0,h_base])(sd.cylinder(d=d_puzz-4*tip, h=h_puzz))
    final -= sd.translate([0,MAX/2-(d_puzz-4*tip)/2,0])(sd.cube([gap,MAX,MAX], center=True))
    top = sd.cylinder(d1=d_puzz, d2=d_puzz-2*ridge-2*gap, h=ridge)
    top -= sd.translate([0,0,-epsilon])(sd.cylinder(d1=d_puzz-4*tip, d2=d_puzz-2*ridge-2*gap-4*tip, h=ridge+2*epsilon))
    top2 = sd.cylinder(d1=d_puzz-2*ridge-2*gap, d2=d_puzz-4*tip-2*gap, h=ridge-2*tip)
    top2 -= sd.translate([0,0,-epsilon])(sd.cylinder(d1=d_puzz-2*ridge-2*gap-4*tip, d2=d_puzz-2*gap-8*tip, h=ridge-2*tip+2*epsilon))
    final += sd.translate([0,0,h_puzz])(top)
    final += sd.translate([0,0,h_puzz+ridge])(top2)
    final -= sd.translate([0,MAX/2,0])(sd.cube([gap,MAX,MAX], center=True))
    cutline = sd.cube([gap, MAX, .8], center=True)
    final -= sd.union()(*[sd.rotate([0,0,i*360/8])(cutline) for i in range(8)])
    return final

def puzzle_box_lid():
    tip = .4
    gap = .1
    d_puzz = 100
    h_puzz = 5
    ridge = 4
    epsilon = 0.01
    MAX = 1000

    final = sd.cylinder(d=d_puzz, h=h_puzz)
    final -= sd.translate([0,0,1])(sd.cylinder(d=d_puzz-4*tip, h=h_puzz))
    final -= sd.translate([0,MAX/2-(d_puzz-4*tip)/2,0])(sd.cube([gap,MAX,MAX], center=True))
    top = sd.cylinder(d=d_puzz, h=2*ridge-4*tip)
    top1 = sd.cylinder(d2=d_puzz-2*ridge, d1=d_puzz-4*tip, h=ridge-2*tip+epsilon)
    top2 = sd.cylinder(d1=d_puzz-2*ridge, d2=d_puzz-4*tip, h=ridge-2*tip+epsilon)
    top -= sd.translate([0,0,0])(top1)
    top -= sd.translate([0,0,ridge-2*tip])(top2)
    final += sd.translate([0,0,h_puzz])(top)
    final -= sd.translate([0,MAX/2,0])(sd.cube([gap,MAX,MAX], center=True))
    cutline = sd.cube([gap, MAX, .8], center=True)
    final -= sd.union()(*[sd.rotate([0,0,i*360/8])(cutline) for i in range(8)])
    return final


if __name__ == '__main__':
    fn = 64
    ridge = 4
    tip = .4

    # CHOOSE one of the following:
    final = puzzle_box_base()
    # final = puzzle_box_lid()

    # This was just to see how they lined up.
    # lid = puzzle_box_lid()
    # lid = sd.mirror([0,0,1])(lid)
    # lid = sd.translate([0,0,50+2*ridge-2*tip+4.4])(lid)
    # final += lid
    final = sd.scad_render(final, file_header=f'$fn={fn};')
    print(final)


