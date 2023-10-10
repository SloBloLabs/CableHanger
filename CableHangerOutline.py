from pcbnew import *
import math

# https://forum.kicad.info/t/draw-line-segment-from-python/7072/5
# https://forum.kicad.info/t/creating-arcs-in-pcbnew-python/28321
# https://python.hotexamples.com/examples/kicad.point/Point/-/python-point-class-examples.html

class CableHangerOutline(ActionPlugin):
    def defaults(self):
        self.name = "CableHangerOutline"
        self.category = "A descriptive category name"
        self.description = "A description of the plugin and what it does"
    
    def Run(self):
        self._board = GetBoard()
        self._center = wxSize(285, 200)

        self.clear()

        #self.RenderCircles()
        #self.RenderPhyllotaxisSpirals()
        
        self.RenderCableHangerOutline()
    
    def RenderCableHangerOutline(self):
        #self.drawLineCSym(-150, -150, 150, -150)
        #self.drawLineCSym( 150, -150, 150,  150)
        
        # Eurorack comb
        self.drawEurorackComb()

        # Other cables comb

        # Tool holes
        
        # Center mounting hole 3/8"
        self.drawCircle(0, 0, 5, 0) # 3/8" = 9,525mm

    def drawEurorackComb(self):
        toothWidth = 6
        gapWidth = 5
        gapHight = 100
        retainerHight = 8
        retainerBump = .5
        n = 27
        chWidth = 27 * gapWidth + (27 + 1) * toothWidth
        
        start_x = -chWidth / 2
        start_y = start_x

        ex = start_x + toothWidth
        ey = start_y
        self.drawLineCSym(start_x, start_y, ex, ey)

        for x in range(n):
            self.drawVerticalCombTooth(ex + x * (toothWidth + gapWidth), ey, toothWidth, gapWidth, gapHight, retainerHight, retainerBump)
        #self.drawArc(-70, -70, -60, -66, -70, -62)
        #self.drawLine(-30, -30, -20, -30)
        #self.drawArc(-20, -30, -15, -25, -20, -20)
        #self.drawLine(-20, -20, -20, -10)
    
    def drawVerticalCombTooth(self, start_x, start_y, toothWidth, gapWidth, gapHight, retainerHight, retainerBump):
        ex = start_x
        ey = start_y + retainerHight
        mx = start_x + retainerBump
        my = int(start_y + retainerHight / 2)
        self.drawArcCSym(start_x, start_y, mx, my, ex, ey)
        sx = ex
        sy = ey
        ex = start_x
        ey = sy + gapHight - retainerHight
        self.drawLineCSym(sx, sy, ex, ey)
        sx = ex
        sy = ey
        ex = sx + gapWidth
        ey = sy
        self.drawLineCSym(sx, sy, ex, ey)
        sx = ex
        sy = ey
        ex = sx
        ey = sy - gapHight + retainerHight
        self.drawLineCSym(sx, sy, ex, ey)
        sx = ex
        sy = ey
        ex = sx
        ey = sy - retainerHight
        mx = sx - retainerBump
        my = int(sy - retainerHight / 2)
        self.drawArcCSym(sx, sy, mx, my, ex, ey)
        sx = ex
        sy = ey
        ex = sx + toothWidth
        ey = sy
        self.drawLineCSym(sx, sy, ex, ey)
    
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
    
    def drawArcCSym(self, start_x, start_y, mid_x, mid_y, end_x, end_y, layer=Edge_Cuts, width=0.1):
        self.drawArc( start_x,  start_y,  mid_x,  mid_y,  end_x,  end_y, layer=Edge_Cuts, width=0.1)
        self.drawArc(-start_x, -start_y, -mid_x, -mid_y, -end_x, -end_y, layer=Edge_Cuts, width=0.1)
    
    def clear(self):
        for drawing in self._board.GetDrawings():
            if drawing.GetLayerName() == 'Edge.Cuts':
                self._board.Remove(drawing)

    def RenderCircles(self):
        libpath = "/Users/olly/Documents/Github/SloBlo_KiCadLibs/footprints/SloBloFP.pretty"
        fpName = "Via 1mm"
        src_type = IO_MGR.GuessPluginTypeFromLibPath(libpath)
        plugin = IO_MGR.PluginFind(src_type)
        
        padSize = 2.6
        padMargin = 1.2
        radStepT = 30
        totalRad = 260

        center = GetBoard().FindFootprintByReference('LS1').GetCenter()

        i = 0
        for rT in range(0, totalRad, radStepT):
            r = rT / 10.0
            c = 2 * math.pi * r
            size = padSize - .05 * r
            N = max(1, math.floor(c / (size + padMargin)))
            for n in range(N):
                theta = 2 * math.pi / N * n
                x = center.x + FromMM(r * math.cos(theta))
                y = center.y + FromMM(r * math.sin(theta))

                i += 1
                fp = plugin.FootprintLoad(libpath, fpName)
                fp.SetReference("P%02d" % i)
                fp.Reference().SetVisible(False)
                fp.SetPosition(VECTOR2I(x, y))

                drillSize = size * 0.6
                pad = fp.Pads()[0]
                pad.SetSize(VECTOR2I(wxSizeMM(size, size)))
                pad.SetDrillSize(VECTOR2I(wxSizeMM(drillSize, drillSize)))
                GetBoard().Add(fp)
    
    def RenderPhyllotaxisSpirals(self):
        N = 250
        base = 3.33
        baseAngle = math.pi * (1 + math.sqrt(5)) / 2. * base
        minPadSize = 1

        center = GetBoard().FindFootprintByReference('LS1').GetCenter()

        for n in range(N):
            r = math.sqrt(n) * 1.5
            theta = baseAngle * n
            x = r * math.cos(theta) + center.x / 1000000.
            y = r * math.sin(theta) + center.y / 1000000.
            padSize = minPadSize + n/250.
            pad = self.CreatePad(padSize, padSize * .5, x, y)
            GetBoard().Add(pad)
    
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
        module.SetPosition(VECTOR2I(wxPointMM(posX, posY)))
        return module

CableHangerOutline().register()
