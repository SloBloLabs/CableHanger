# pcbnew console

Prerequisites:
smallest unit in pcbnew is 1 nanometer
1 nanometer = 10^(-9) meter = 10^(-6) mm

'PCB_IU_PER_MM': 1000000.0
helps with that conversion:

10 mm = 10 * PCB_IU_PER_MM = 10000000 nanometer


import math

from pcbnew import *

b = GetBoard()

###

start = VECTOR2I(wxSizeMM(100, 100))
end = VECTOR2I(wxSizeMM(200, 100))
line = PCB_SHAPE(b, SHAPE_T_SEGMENT)
line.SetStart(start)
line.SetEnd(end)
line.SetWidth(FromMM(.1))
line.SetLayer(Edge_Cuts)
b.Add(line)
Refresh()

###

circle = PCB_SHAPE(b, SHAPE_T_CIRCLE)
start = VECTOR2I(wxSizeMM(100, 100))
end = VECTOR2I(wxSizeMM(150, 100))
circle.SetStart(start)
circle.SetEnd(end)
circle.SetWidth(FromMM(.1))
circle.SetLayer(Edge_Cuts)
b.Add(circle)
Refresh()

###

arc = PCB_SHAPE(b, SHAPE_T_ARC)
start = VECTOR2I(wxSizeMM(100, 50))
mid = VECTOR2I(wxSizeMM(100, 100))
end = VECTOR2I(wxSizeMM(200, 200))
arc.SetArcGeometry(start, mid, end)
arc.SetLayer(Edge_Cuts)
# arc.SetWidth(int(0.1 * PCB_IU_PER_MM))
arc.SetWidth(FromMM(.1))
b.Add(arc)
Refresh()

###

c = [[50,50], [150, 50], [150, 150], [50, 150]]
for p in range(len(c)):
    start = VECTOR2I(wxSizeMM(c[p][0], c[p][1]))
    p_end = (p + 1) % len(c)
    end = VECTOR2I(wxSizeMM(c[p_end][0], c[p_end][1]))
    line = PCB_SHAPE(b, SHAPE_T_SEGMENT)
    line.SetStart(start)
    line.SetEnd(end)
    line.SetWidth(FromMM(.1))
    line.SetLayer(Edge_Cuts)
    b.Add(line)
Refresh()

###
### Writing a plugin
MyAwesomePlugin
BasicShape
RoundCorners