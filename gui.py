import wx
from core import *
import random


dm=DynModule()

dm.setLayer("conv1",lambda x:x,{"x":"input"})
dm.setLayer("pool1",lambda x:x,{"x":"conv1"})
dm.setLayer("conv2",lambda x:x,{"x":"pool1"})
dm.setLayer("pool2",lambda x:x,{"x":"conv2"})

dm.setLayer("output",lambda x:x,{"x":"pool2"})


class GraphPanel(wx.Panel):
    def __init__(self, parent,module=dm):
        super(GraphPanel, self).__init__(parent, size=(600, 400))
        self.SetBackgroundColour(wx.WHITE)
        self.module=module
        for k,v in module.layers.items():
            v["pos"]=[int(random.random()*200),int(random.random()*200)]
        
        self.dragging=False
        self.selected = None
        self.drag_offset = (0, 0)
        self.translation=(0,0)
        
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_LEFT_DOWN, self.on_left_down)
        self.Bind(wx.EVT_LEFT_UP, self.on_left_up)
        self.Bind(wx.EVT_MOTION, self.on_motion)
        self.organize()
        
    def draw_connection(self,dc, src,dst):
        pos_a=src["pos"]
        pos_b=dst["pos"]
        
        x1, y1 = pos_a[0] + 50, pos_a[1] + 15  # Punto sul lato destro di a
        x2, y2 = pos_b[0], pos_b[1] + 15  # Punto sul lato sinistro di b
        
        # Calcola i punti di controllo per creare una curva liscia
        control_x1 = (x1 + x2) // 2
        control_y1 = y1
        control_x2 = control_x1
        control_y2 = y2
        
        dc.SetPen(wx.Pen(wx.LIGHT_GREY, 2))  # Cambia il colore della penna qui
    
        # Disegna la spline
        dc.DrawSpline([(x1, y1), (control_x1, control_y1), (control_x2, control_y2), (x2, y2)])
        






    def on_paint(self, event):
        dc = wx.PaintDC(self)
        
        dc.SetUserScale(1, 1)
        dc.SetDeviceOrigin(*self.translation)
        
        dc.Clear()
        dc.SetPen(wx.Pen(wx.BLACK, 2))
        dc.SetBrush(wx.Brush(wx.BLUE))
        for k,l in self.module.layers.items():
            pos=l["pos"]
            dc.DrawRectangle(pos[0], pos[1], 50, 30)
            dc.DrawText(k, pos[0] + 5, pos[1] + 5)            
            for ik,iv in l["inputs"].items():
                il=self.module.layers[iv]
                self.draw_connection(dc,il,l)
            
    def device2world(self,pos):
        x,y=pos
        ox,oy=self.translation
        return [x-ox,y-oy]
    def world2device(self,pos):
        x,y=pos
        ox,oy=self.translation
        return [x+ox,y+oy]
        
            

    def pick(self,x,y):
        for k,v in self.module.layers.items():
            pos=v["pos"]
            if pos[0] <= x <= pos[0] + 50 and pos[1] <= y <= pos[1] + 30:
                return k
    @property
    def layer(self):
        return self.module.layers.get(self.selected,None)
        

    def on_left_down(self, event):
        x, y =self.device2world(event.GetPosition())
        self.selected=self.pick(x,y)
        if self.selected:
            pos=self.layer["pos"]
            self.drag_offset = (pos[0] - x, pos[1] - y)
        else:
            self.drag_offset = x, y
        self.dragging=True

    def on_left_up(self, event):
        self.selected=None
        self.dragging=False

    def on_motion(self, event):
        x, y = self.device2world(event.GetPosition())
        if self.dragging:
            if self.layer:
                self.layer["pos"]=(x + self.drag_offset[0], y + self.drag_offset[1])
            else:
                self.translation=self.world2device((x-self.drag_offset[0],y-self.drag_offset[1]))
            self.Refresh()
        
        
    def organize(self):
        def place(layer,olayer=None):
            op=self.module.layers.get(olayer,{}).get("pos",[800,300])
            self.module.layers[layer]["pos"]=[op[0]-120,op[1]+int(random.random()*200)-100]
            for k,v in  self.module.layers[layer]["inputs"].items():
                place(v,layer)
        place("output")
            

class MainFrame(wx.Frame):
    def __init__(self):
        super(MainFrame, self).__init__(None, title="Graph", size=(800, 600))
        panel = GraphPanel(self)
        self.Show()

if __name__ == "__main__":
    app = wx.App()
    frame = MainFrame()
    app.MainLoop()
