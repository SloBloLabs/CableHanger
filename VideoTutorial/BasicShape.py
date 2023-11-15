from pcbnew import *
import math

class BasicShape(ActionPlugin):
    def defaults(self):
        self.name = "BasicShape"
        self.category = "A descriptive category name"
        self.description = "A description of the plugin and what it does"
    
    def Run(self):
        self._board = GetBoard()
        self._center = wxSize(150, 100)

        self.drawLine(0, 0, 50, 0)
        self.drawCircle(0, 0, 00, 50)
        self.drawArc(0, 0, 0, -50, 50, -50)
    
    def drawLine(self, start_x, start_y, end_x, end_y, layer=Edge_Cuts, width=0.1):
        line = PCB_SHAPE(self._board, SHAPE_T_SEGMENT)
        line.SetStart(VECTOR2I(wxSizeMM(start_x + self._center.x, start_y + self._center.y)))
        line.SetEnd  (VECTOR2I(wxSizeMM(end_x   + self._center.x, end_y   + self._center.y)))
        line.SetWidth(FromMM(.1))
        line.SetLayer(layer)
        self._board.Add(line)
    
    def drawCircle(self, start_x, start_y, end_x, end_y, layer=Edge_Cuts, width=0.1):
        circle = PCB_SHAPE(self._board, SHAPE_T_CIRCLE)
        circle.SetStart(VECTOR2I(wxSizeMM(start_x + self._center.x, start_y + self._center.y)))
        circle.SetEnd  (VECTOR2I(wxSizeMM(end_x   + self._center.x, end_y   + self._center.y)))
        circle.SetWidth(FromMM(.1))
        circle.SetLayer(layer)
        self._board.Add(circle)
    
    def drawArc(self, start_x, start_y, mid_x, mid_y, end_x, end_y, layer=Edge_Cuts, width=0.1):
        arc = PCB_SHAPE(self._board, SHAPE_T_ARC)
        start = VECTOR2I(wxPointMM(start_x + self._center.x, start_y + self._center.y))
        mid   = VECTOR2I(wxPointMM(mid_x   + self._center.x, mid_y   + self._center.y))
        end   = VECTOR2I(wxPointMM(end_x   + self._center.x, end_y   + self._center.y))
        arc.SetArcGeometry(start, mid, end)
        arc.SetLayer(layer)
        arc.SetWidth(FromMM(.1))
        self._board.Add(arc)

BasicShape().register()
