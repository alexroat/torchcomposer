import wx

class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        super(MyFrame, self).__init__(parent, title=title, size=(300, 200))
        self.panel = wx.Panel(self)
        self.Bind(wx.EVT_CLOSE, self.on_close)
        self.init_ui()

    def init_ui(self):
        # Aggiungi qui i tuoi widget e layout
        wx.StaticText(self.panel, label="Ciao, wxPython!", pos=(20, 20))

        # Imposta l'icona dell'applicazione
        self.SetIcon(wx.Icon('torchcomposer_logo.png'))

    def on_close(self, event):
        self.Destroy()

if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame(None, title="Finestra di esempio con wxPython")
    frame.Show()
    app.MainLoop()
