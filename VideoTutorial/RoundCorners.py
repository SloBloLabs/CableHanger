from pcbnew import *
import math

class RoundCorners(ActionPlugin):
    def defaults(self):
        self.name = "RoundCorners"
        self.category = "A descriptive category name"
        self.description = "A description of the plugin and what it does"
    
    def Run(self):
        self._board = GetBoard()
        self._center = wxSize(150, 100)

        self.clear()

        self.DrawRoundCorners()
    
    def DrawRoundCorners(self):
        sideLength = 50
        cornerRadius = 5

        start_x = -sideLength / 2
        start_y = start_x

        # upper left corner + lower right corner
        sx = start_x
        sy = start_y + cornerRadius
        mx = start_x + cornerRadius * (1 - math.cos(math.pi/4))
        my = start_y + cornerRadius * (1 - math.sin(math.pi/4))
        ex = start_x + cornerRadius
        ey = start_y
        self.drawArcCSym(sx, sy, mx, my, ex, ey)

        # upper and lower border
        sx = ex; sy = ey
        ex = sx + sideLength - 2 * cornerRadius
        ey = sy
        self.drawLineCSym(sx, sy, ex, ey)
        
        # upper right and lower left corner
        sx = ex; sy = ey
        mx = sx + cornerRadius * math.cos(math.pi/4)
        my = sy + cornerRadius * (1 - math.sin(math.pi/4))
        ex = sx + cornerRadius
        ey = sy + cornerRadius
        self.drawArcCSym(sx, sy, mx, my, ex, ey)

        # side borders
        sx = ex; sy = ey
        ex = sx
        ey = sy + sideLength - 2 * cornerRadius
        self.drawLineCSym(sx, sy, ex, ey)
    
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
    
    def drawLineCSym(self, start_x, start_y, end_x, end_y, layer=Edge_Cuts, width=0.1):
        self.drawLine( start_x,  start_y,  end_x,  end_y, layer, width)
        self.drawLine(-start_x, -start_y, -end_x, -end_y, layer, width)
    
    def drawCircleCSym(self, start_x, start_y, end_x, end_y, layer=Edge_Cuts, width=0.1):
        self.drawCircle( start_x,  start_y,  end_x,  end_y, layer, width)
        self.drawCircle(-start_x, -start_y, -end_x, -end_y, layer, width)
    
    def drawArcCSym(self, start_x, start_y, mid_x, mid_y, end_x, end_y, layer=Edge_Cuts, width=0.1):
        self.drawArc( start_x,  start_y,  mid_x,  mid_y,  end_x,  end_y, layer, width)
        self.drawArc(-start_x, -start_y, -mid_x, -mid_y, -end_x, -end_y, layer, width)

    def clear(self):
        for drawing in self._board.GetDrawings():
            if drawing.GetLayerName() == 'Edge.Cuts':
                self._board.Remove(drawing)

RoundCorners().register()