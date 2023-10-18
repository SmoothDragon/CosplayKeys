#!/usr/bin/env python

import solid as sd
import numpy as np
import pathlib
import tempfile
import subprocess
import shlex

def scad2svg(scad_obj, fn):
    '''Use OpenSCAD to create SVG file from SCAD file.
    Write and read from temporary files.
    TODO: Is there a way to bypass using tempfiles?
    '''
    file_scad = tempfile.NamedTemporaryFile(delete=False)
    file_svg = tempfile.NamedTemporaryFile(delete=False)
    # Note that when openscad tries to import_ a SVG file, it will look for it in /tmp
    # Thus we have to create a symlink to the temp file.
    tmpfile = pathlib.Path(file_scad.name)
    tmpname = pathlib.Path(tmpfile.name).symlink_to(tmpfile)

    sd.scad_render_to_file(scad_obj, filepath=file_scad.name, file_header=f'$fn={fn};')
    command = f'openscad --export-format=svg {tmpname} -o {file_svg.name}'
    subprocess.run(shlex.split(command))
    str_svg = open(file_svg.name).read()
    return str_svg

class scadSVG:
    def __init__(self, scad_obj, fn=256, stroke=None, fill=None, strokewidth=None):
        self.fn = fn
        str_svg = scad2svg(scad_obj, self.fn)
        self.init_scadSVG_attrs(str_svg)
        self.set_scadSVG_path_attrs(0, stroke, fill, strokewidth)

    def init_scadSVG_attrs(self, str_svg):
        '''Extract SVG dimensions and path.
        TODO: This function is fragile. It would be better with a parser.
        '''
        svglist = str_svg.splitlines()
        info = svglist[2].split()
        self.xmin = float(info[3][9:])
        self.ymin = float(info[4])
        self.width = float(info[5])
        self.height = float(info[6][:-1])
        self.paths = [ svglist[4:-1] ]

    def get_scadSVG_path_attrs(self, scadSVGpath_idx):
        line = self.paths[scadSVGpath_idx][-1].split()
        stroke = line[1][8:-1]
        fill = line[2][6:-1]
        strokewidth = float(line[3][14:-3])
        return {
            'stroke':stroke,
            'fill':fill,
            'stroke-width':strokewidth,
            }

    def set_scadSVG_path_attrs(self, scadSVGpath_idx=None, stroke=None, fill=None, strokewidth=None):
        '''Update path attributes.
        "None" or "none" is an acceptable fill.
        TODO: Since this is updating in place, it might be better written another way.
        TODO: If index is one, update attibute in all paths.
        TODO: Add fill-opacity as an option.
        '''
        path_attrs = self.get_scadSVG_path_attrs(scadSVGpath_idx)
        stroke = path_attrs['stroke'] if stroke is None else stroke
        fill = path_attrs['fill'] if fill is None else fill
        strokewidth = path_attrs['stroke-width'] if strokewidth is None else strokewidth
        self.paths[scadSVGpath_idx][-1] = f'" stroke="{stroke}" fill="{fill}" stroke-width="{strokewidth}"/>'

    def __add__(self, other):
        xmax = max(self.xmin + self.width, other.xmin + other.width)
        ymax = max(self.ymin + self.height, other.ymin + other.height)
        self.xmin = min(self.xmin, other.xmin)
        self.ymin = min(self.ymin, other.ymin)
        self.width = xmax - self.xmin
        self.height = ymax - self.ymin
        self.paths += other.paths
        return self

    def __str__(self):
        svg_lines = [
        '<?xml version="1.0" standalone="no"?>',
        '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">',
        f'<svg width="{self.width}mm" height="{self.height}mm" viewBox="{self.xmin} {self.ymin} {self.width} {self.height}" xmlns="http://www.w3.org/2000/svg" version="1.1">',
        ]
        for path in self.paths:
            svg_lines += path
        svg_lines.append('</svg>')
        return '\n'.join(svg_lines)


import solid as sd


# Useful 2D functions

def halfPlane(direction, D=1000):
    r'''Create a 2D half plane. Choose D large enough to be "infinity".
    >>> sd.scad_render(halfPlane('N'))
    '\n\ntranslate(v = [0, 1000]) {\n\tsquare(center = true, size = 2000);\n}'
    '''
    planetype = {
        'N':( 0,  D),
        'S':( 0, -D),
        'E':( D,  0),
        'W':(-D,  0),
        'U':( 0,  D),
        'D':( 0, -D),
        'R':( D,  0),
        'L':(-D,  0),
        }
    plane = sd.square(2*D, center=True)
    plane = sd.translate(planetype[direction])(plane)
    return plane

def sector(angle, r=0, D=1000):
    R = r/np.tan(angle/2/360*np.pi)/2
    piece = halfPlane('U', D=D)
    if r>0:
        piece -= sd.circle(R)
    piece = sd.intersection()(piece, sd.rotate([0,0,angle-180])(piece))
    if r>0:
        piece += sd.translate([R,r])(sd.circle(r))
    return piece

def annulus(R, w, position='center'):
    '''Annulus or radius R with line of width w centered on perimeter
    '''
    linetype = {
        'center': (R+w/2, R-w/2),
        'inner': (R, R-w),
        'outer': (R+w, R),
        }
    R_outer, R_inner = linetype[position]
    figure = sd.circle(R_outer)
    figure -= sd.circle(R_inner)
    return figure

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

def hexagram(R):
    wedge = sd.circle(R, segments=3)
    wedge += sd.rotate([0,0,180])(wedge),
    return wedge

if __name__ == '__main__':
    import doctest
    doctest.testmod()
