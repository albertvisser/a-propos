import wx
from apomixin import Apomixin

class Page(wx.Panel):
    def __init__(self,parent,id,mf=None):
        wx.Panel.__init__(self,parent,id)
        print "new page",self
        self.txt = wx.TextCtrl(self,-1,style=wx.TE_MULTILINE)
        self.txt.Bind(wx.EVT_KEY_DOWN, mf.on_key)
        ## self.Bind(wx.EVT_TEXT, self.OnEvtText, self.txt)
        sizer0 = wx.BoxSizer(wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(self.txt,1,wx.EXPAND)
        sizer0.Add(sizer1,1,wx.EXPAND)
        self.SetSizer(sizer0)
        self.SetAutoLayout(True)
        sizer0.Fit(self)
        sizer0.SetSizeHints(self)
        self.Layout()

class MainFrame(wx.Frame,Apomixin):
    def __init__(self,parent,id):
        wx.Frame.__init__(self,parent,id,"Apropos...") # ,size=(800,500))
        self.Bind(wx.EVT_CLOSE, self.afsl)
        pnl = wx.Panel(self,-1)
        self.nb = wx.Notebook(pnl,-1)
        self.nb.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.page_changed)
        self.nb.Bind(wx.EVT_LEFT_DCLICK, self.onLeftDblClick)
        self.nb.Bind(wx.EVT_MIDDLE_DOWN, self.onLeftDblClick)
        self.load_notes()
        if self.apodata:
            for i,x in self.apodata.items():
                self.newtab(titel=x[0],note=x[1])
            self.nb.ChangeSelection(0)
        else:
            self.newtab()
            self.current = 0
        ## self.nb.GetPage(0).txt.SetFocus()
        sizer0 = wx.BoxSizer(wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(self.nb,1,wx.EXPAND)
        sizer0.Add(sizer1,1,wx.EXPAND)
        pnl.SetSizer(sizer0)
        pnl.SetAutoLayout(True)
        sizer0.Fit(pnl)
        sizer0.SetSizeHints(pnl)
        pnl.Layout()
        self.Bind(wx.EVT_CLOSE,self.afsl)
        self.Show()

    def page_changed(self,event=None):
        n = self.nb.GetPageCount()
        s = self.nb.GetSelection()
        self.current = event.GetSelection()
        currentpage = self.nb.GetPage(self.current)
        ## currentpage.SetFocus()
        currentpage.txt.SetFocus()
        event.Skip()

    def on_key(self,event=None):
        skip = True
        keycode = event.GetKeyCode()
        if event.GetModifiers() == wx.MOD_CONTROL: # evt.ControlDown()
            if keycode == wx.WXK_LEFT or keycode == wx.WXK_NUMPAD_LEFT: #  keycode == 314
                self.nb.AdvancePage(False)
            elif keycode == wx.WXK_RIGHT or keycode == wx.WXK_NUMPAD_RIGHT: #  keycode == 316
                self.nb.AdvancePage()
            elif keycode == 78: # Ctrl-N
                self.newtab()
            elif keycode == 87: # Ctrl-W
                self.closetab()
                skip = False
            elif keycode == 83: # Ctrl-Q
                self.afsl()
            elif keycode == 81: # Ctrl-Q
                self.afsl()
                self.Destroy()
        if event and skip:
            event.Skip()

    def onLeftDblClick(self,event=None):
        self.x = event.GetX()
        self.y = event.GetY()
        item, flags = self.nb.HitTest((self.x, self.y))
        self.nb.DeletePage(item)
        event.Skip()

    def newtab(self,titel=None,note=None):
        ## print("create new tab")
        nieuw = self.nb.GetPageCount()
        if titel is None: titel = str(nieuw)
        newpage = Page(self.nb,-1,mf=self)
        ## print("new page created")
        if note is not None:
            newpage.txt.SetValue(note)
        ## print("adding new page")
        self.nb.AddPage(newpage,titel)
        ## print "new page added"
        self.nb.SetSelection(nieuw)

    def closetab(self):
        pagetodelete = self.current
        aant = self.nb.GetPageCount()
        print aant
        if aant == 1:
            self.afsl()
            self.Destroy()
        else:
            ## print "closing page", pagetodelete
            ## self.nb.AdvanceSelection(False)
            self.nb.DeletePage(pagetodelete)

    def afsl(self,event=None):
        self.apodata = {}
        for i in range(self.nb.GetPageCount()):
            page = self.nb.GetPage(i)
            title = self.nb.GetPageText(i)
            text = page.txt.GetValue()
            self.apodata[i] = (title,text)
        self.save_notes()
        if event:
            event.Skip()


class Main():
    def __init__(self):
        app = wx.App(redirect=False) # True) # ,filename="apropos.log")
        frm = MainFrame(None, -1)
        app.MainLoop()

if __name__ == "__main__":
    Main()

# probreg.pyw:
# bij selecteren van een andere tab:
# - on leftdown - doet uitzoeken op welke tab geklikt is en kijk of deze de huidige is
#       als op de huidige geklikt is dan tab "afsluiten"
# - on leftup - focus op de huidige?
# ik denk dat tussen de onleftdown en de onleftup vindt kennelijk het page changen plaats
