from pcbnew import *
import math

# https://forum.kicad.info/t/draw-line-segment-from-python/7072/5
# https://forum.kicad.info/t/creating-arcs-in-pcbnew-python/28321
# https://python.hotexamples.com/examples/kicad.point/Point/-/python-point-class-examples.html

class CableHolderOutline(ActionPlugin):
    def defaults(self):
        self.name = "CableHolderOutline"
        self.category = "A descriptive category name"
        self.description = "A description of the plugin and what it does"
    
    def Run(self):
        self._board = GetBoard()
        self._center = wxSize(285, 200)

        self.clear()
        
        self.RenderCableHolderCutEdge()

        self.RenderToolHoles()

        self.RenderLogo()
    
    def RenderCableHolderCutEdge(self):
        self._cornerRadius = 3
        self._gapHeight = 85

        # Eurorack comb
        loc = self.drawEurorackComb()

        # Other cables comb
        self.drawOthersComb(loc[0][0], loc[0][1], loc[1])
        
        # Center mounting hole 3/8"
        self.drawCircle(0, 0, 5, 0) # 3/8" = 9,525mm
    
    def RenderToolHoles(self):
        # Tool holes
        toolHolesRadius = 32
        orthoShift      = 5

        pad = self.CreatePad(12, 10, -toolHolesRadius, -toolHolesRadius); self._board.Add(pad)
        pad = self.CreatePad(15, 13,  toolHolesRadius, -toolHolesRadius); self._board.Add(pad)
        pad = self.CreatePad(12, 10,  toolHolesRadius,  toolHolesRadius); self._board.Add(pad)
        pad = self.CreatePad(15, 13, -toolHolesRadius,  toolHolesRadius); self._board.Add(pad)
        
        pad = self.CreatePad(11, 9, 0                            , -toolHolesRadius - orthoShift); self._board.Add(pad)
        pad = self.CreatePad(11, 9, 0                            ,  toolHolesRadius + orthoShift); self._board.Add(pad)
        pad = self.CreatePad(11, 9,  toolHolesRadius + orthoShift,                             0); self._board.Add(pad)
        pad = self.CreatePad(11, 9, -toolHolesRadius - orthoShift,                             0); self._board.Add(pad)

    def RenderLogo(self):
        libpath = "/Users/olly/Documents/Github/SloBlo_KiCadLibs/footprints/SloBloFP.pretty"
        fpName = "SloBloLogo_230x280"
        src_type = IO_MGR.GuessPluginTypeFromLibPath(libpath)
        plugin = IO_MGR.PluginFind(src_type)

        fp = plugin.FootprintLoad(libpath, fpName)
        fp.SetReference("SloBloLogo")
        fp.Reference().SetVisible(False)
        fp.SetPosition(VECTOR2I(wxSizeMM(self._center.x, self._center.y)))
        self._board.Add(fp)

    def drawEurorackComb(self):
        toothWidth = 10
        gapWidth = 5
        retainerHeight = 5
        retainerBump = .5
        n = 19
        chWidth = n * gapWidth + (n + 1) * toothWidth

        start_x = -chWidth / 2
        start_y = start_x

        # 1st corner
        sx = start_x
        sy = start_y + self._cornerRadius
        mx = start_x + self._cornerRadius * (1 - math.cos(math.pi/4))
        my = start_y + self._cornerRadius * (1 - math.sin(math.pi/4))
        ex = start_x + self._cornerRadius
        ey = start_y
        self.drawArcCSym(sx, sy, mx, my, ex, ey)

        sx = ex; sy = ey
        ex = start_x + toothWidth
        ey = start_y
        self.drawLineCSym(sx, sy, ex, ey)

        end = None

        for x in range(n):
            end = self.drawVerticalCombTooth(ex + x * (toothWidth + gapWidth), ey, toothWidth, gapWidth, retainerHeight, retainerBump)
        
            sx_ = end[0]; sy_ = end[1]
            ex_ = sx_ + toothWidth
            ey_ = sy_
#
            if x == (n - 1):
                ex_ -= self._cornerRadius
            
            self.drawLineCSym(sx_, sy_, ex_, ey_)
        
        ## 2nd corner
        sx = ex_; sy = ey_
        mx = sx + self._cornerRadius * math.cos(math.pi/4)
        my = sy + self._cornerRadius * (1 - math.sin(math.pi/4))
        ex = sx + self._cornerRadius
        ey = sy + self._cornerRadius
        self.drawArcCSym(ex, ey, mx, my, sx, sy)

        return ((ex, ey), chWidth)

    def drawOthersComb(self, start_x, start_y, chHeight):
        toothWidth = 10
        gapWidth = 7
        retainerHeight = 5
        retainerBump = .5

        ocHeight = chHeight - 2 * (self._gapHeight + self._cornerRadius)

        n = math.floor((ocHeight - toothWidth) / (toothWidth + gapWidth))
        
        gapDistance = n * gapWidth + (n - 1) * toothWidth

        rest = ocHeight - gapDistance

        sx = start_x; sy = start_y
        ex = sx
        ey = sy + self._gapHeight + (rest / 2)
        self.drawLineCSym(start_x, start_y, ex, ey)

        for x in range(n):
            end = self.drawHorizontalCombTooth(ex, ey + x * (toothWidth + gapWidth), toothWidth, gapWidth, retainerHeight, retainerBump)
        
        sx = end[0]; sy = end[1]
        ex = sx
        ey = -start_y
        self.drawLineCSym(sx, sy, ex, ey)
    
    def drawVerticalCombTooth(self, start_x, start_y, toothWidth, gapWidth, retainerHeight, retainerBump):
        ex = start_x
        ey = start_y + retainerHeight
        mx = start_x + retainerBump
        my = int(start_y + retainerHeight / 2)
        self.drawArcCSym(start_x, start_y, mx, my, ex, ey)
        sx = ex; sy = ey
        ex = start_x
        ey = sy + self._gapHeight - retainerHeight
        self.drawLineCSym(sx, sy, ex, ey)
        sx = ex; sy = ey
        mx = int(sx + gapWidth / 2)
        my = int(sy + gapWidth / 2)
        ex = sx + gapWidth
        ey = sy
        self.drawArcCSym(sx, sy, mx, my, ex, ey)
        sx = ex; sy = ey
        ex = sx
        ey = sy - self._gapHeight + retainerHeight
        self.drawLineCSym(sx, sy, ex, ey)
        sx = ex; sy = ey
        ex = sx
        ey = sy - retainerHeight
        mx = sx - retainerBump
        my = int(sy - retainerHeight / 2)
        self.drawArcCSym(sx, sy, mx, my, ex, ey)
        return (ex, ey)
    
    def drawHorizontalCombTooth(self, start_x, start_y, toothWidth, gapWidth, retainerHeight, retainerBump):
        ex = start_x - retainerHeight
        ey = start_y
        mx = int(start_x - retainerHeight / 2)
        my = start_y + retainerBump
        self.drawArcCSym(start_x, start_y, mx, my, ex, ey)
        sx = ex; sy = ey
        ex = sx - self._gapHeight + retainerHeight
        ey = sy
        self.drawLineCSym(sx, sy, ex, ey)
        sx = ex; sy = ey
        mx = int(sx - gapWidth / 2)
        my = int(sy + gapWidth / 2)
        ex = sx
        ey = sy + gapWidth
        self.drawArcCSym(sx, sy, mx, my, ex, ey)
        sx = ex; sy = ey
        ex = sx + self._gapHeight - retainerHeight
        ey = sy
        self.drawLineCSym(sx, sy, ex, ey)
        sx = ex; sy = ey
        ex = sx + retainerHeight
        ey = sy
        mx = int(sx + retainerHeight / 2)
        my = sy - retainerBump
        self.drawArcCSym(sx, sy, mx, my, ex, ey)
        sx = ex; sy = ey
        ex = sx
        ey = sy + toothWidth
        self.drawLineCSym(sx, sy, ex, ey)
        return (ex, ey)
    
    def drawLine(self, start_x, start_y, end_x, end_y, layer=Edge_Cuts, width=0.1):
        line = PCB_SHAPE(self._board, SHAPE_T_SEGMENT)
        line.SetStart(VECTOR2I(wxSizeMM(start_x + self._center.x, start_y + self._center.y)))
        line.SetEnd  (VECTOR2I(wxSizeMM(end_x   + self._center.x, end_y   + self._center.y)))
        line.SetWidth(int(width * PCB_IU_PER_MM)) # PCB_IU_PER_MM = 1000000
        line.SetLayer(layer)
        self._board.Add(line)
    
    def drawCircle(self, start_x, start_y, end_x, end_y, layer=Edge_Cuts, width=0.1):
        circle = PCB_SHAPE(self._board, SHAPE_T_CIRCLE)
        circle.SetStart(VECTOR2I(wxSizeMM(start_x + self._center.x, start_y + self._center.y)))
        circle.SetEnd  (VECTOR2I(wxSizeMM(end_x   + self._center.x, end_y   + self._center.y)))
        circle.SetWidth(int(width * PCB_IU_PER_MM)) # PCB_IU_PER_MM = 1000000
        circle.SetLayer(layer)
        self._board.Add(circle)
    
    def drawArc(self, start_x, start_y, mid_x, mid_y, end_x, end_y, layer=Edge_Cuts, width=0.1):
        arc = PCB_SHAPE(self._board)
        arc.SetShape(SHAPE_T_ARC)
        start = VECTOR2I(wxPointMM(start_x + self._center.x, start_y + self._center.y))
        mid = VECTOR2I(wxPointMM(mid_x     + self._center.x, mid_y   + self._center.y))
        end = VECTOR2I(wxPointMM(end_x     + self._center.x, end_y   + self._center.y))
        arc.SetArcGeometry(start, mid, end)
        arc.SetLayer(layer)
        arc.SetWidth(int(width * PCB_IU_PER_MM))
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
    
    def CreatePad(self, padSize=2, drillSize=1, posX=0, posY=0):
        #https://atomic14.com/2022/10/24/kicad-python-scripting-cheat-sheet-copy.html
        module = FOOTPRINT(GetBoard())
        pad = PAD(module)
        pad.SetSize(VECTOR2I(wxSizeMM(padSize, padSize)))
        pad.SetDrillSize(VECTOR2I(wxSizeMM(drillSize, drillSize)))
        pad.SetShape(PAD_SHAPE_CIRCLE)
        pad.SetAttribute(PAD_ATTRIB_PTH)
        # remove mask to darken backside
        pad.SetLayerSet(pad.PTHMask().RemoveLayer(B_Mask))
        pad.SetPosition(VECTOR2I(wxPointMM(0, 0)))
        #pcb_pad.SetNetCode(net.GetNetCode())
        module.Add(pad)
        module.SetPosition(VECTOR2I(wxPointMM(posX + self._center.x, posY + self._center.y)))
        return module
    
    def clear(self):
        for drawing in self._board.GetDrawings():
            if drawing.GetLayerName() == 'Edge.Cuts':
                self._board.Remove(drawing)
        
        # TODO: Footprint Housekeeping
        #self._board.DeleteAllFootprints() # this kills KiCad for unknown reason

CableHolderOutline().register()
