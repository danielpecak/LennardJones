#!/usr/bin/env python
# -*- coding: utf-8 -*-
import svgwrite

def draw_atom(dwg,x,y):
    """Draws an atom in the svgwrite object 'dwg' at coordinates (x,y)."""
    # base gradient
    gradient1 = dwg.defs.add(dwg.radialGradient(center=(0.35,0.35),r=0.7))
    gradient1.add_stop_color(0,'rgb(255,255,255)')
    gradient1.add_stop_color(0.5,'rgb(127,153,191)')
    gradient1.add_stop_color(0.75,'rgb(63,102,159)')
    gradient1.add_stop_color(0.88,'rgb(31,76,143)')
    gradient1.add_stop_color(0.94,'rgb(15,63,135)')
    gradient1.add_stop_color(0.97,'rgb(7,57,131)')
    gradient1.add_stop_color(1.0,'rgb(0,51,128)')
    # boundary gradient
    gradient2 = dwg.defs.add(dwg.radialGradient(r=1.05))
    gradient2.add_stop_color(0, 'white',opacity=0)
    gradient2.add_stop_color(0.33,'rgb(167,185,212)',opacity=0.078)
    gradient2.add_stop_color(0.43,'rgb(33,82,154)',opacity=0.35)
    gradient2.add_stop_color(0.5,'rgb(0,0,0)',opacity=0.4)
    gradient2.add_stop_color(1, 'rgb(42,47,159)',opacity=0.855)

    circle1 = dwg.circle(center=(x, y), r='5', fill=gradient1.get_paint_server())
    circle2 = dwg.circle(center=(x, y), r='5', fill=gradient2.get_paint_server())

    dwg.add(circle1)
    dwg.add(circle2)

def draw_atom_red(dwg,x,y):
    """Draws an atom in the svgwrite object 'dwg' at coordinates (x,y)."""
    # base gradient
    gradient1 = dwg.defs.add(dwg.radialGradient(center=(0.35,0.35),r=0.7))
    gradient1.add_stop_color(0,   'rgb(255,255,255)')
    gradient1.add_stop_color(0.5, 'rgb(210,104,0)')
    gradient1.add_stop_color(0.75,'rgb(198,67,35)')
    gradient1.add_stop_color(0.88,'rgb(175,47,0)')
    gradient1.add_stop_color(0.94,'rgb(171,20,0)')
    gradient1.add_stop_color(0.97,'rgb(159,20,0)')
    gradient1.add_stop_color(1.0, 'rgb(128,20,0)')
    # boundary gradient
    gradient2 = dwg.defs.add(dwg.radialGradient(r=1.05))
    gradient2.add_stop_color(0,   'white',opacity=0)
    gradient2.add_stop_color(0.33,'rgb(233,82,0)',opacity=0.078)
    gradient2.add_stop_color(0.43,'rgb(155,31,0)',opacity=0.35)
    gradient2.add_stop_color(0.5, 'rgb(0,0,0)',opacity=0.4)
    gradient2.add_stop_color(1,   'rgb(143,29,0)',opacity=0.855)

    circle1 = dwg.circle(center=(x, y), r='5', fill=gradient1.get_paint_server())
    circle2 = dwg.circle(center=(x, y), r='5', fill=gradient2.get_paint_server())

    dwg.add(circle1)
    dwg.add(circle2)






with open('coords_start','r') as f:
    coords = f.readlines()
coords = coords[:-1]

# Get ready to draw...
dwg = svgwrite.Drawing(filename='coords_start.svg')
dwg.viewbox(width=400, height=400)
# ...draw atoms...
for c in coords:
    x,y = map(float,c[:-1].split(' '))
    x = 10*x
    y = 10*y
    draw_atom_red(dwg,x,y)
# ...save file
dwg.save()

with open('coords_end','r') as f:
    coords = f.readlines()
coords = coords[:-1]

# Get ready to draw...
dwg = svgwrite.Drawing(filename='coords_end.svg')
dwg.viewbox(width=400, height=400)
# ...draw atoms...
for c in coords:
    x,y = map(float,c[:-1].split(' '))
    x = 10*x
    y = 10*y
    if x<0.0:
        x += 200
    if y<0.0:
        y += 200
    draw_atom(dwg,x,y)
# ...save file
dwg.save()
