import os
import sys
import wx
from apomixin import Apomixin
HERE = os.path.split(__file__)[0]

class Page(wx.Panel):
    def __init__(self,parent,id,mf=None):
        wx.Panel.__init__(self,parent,id)
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

class CheckDialog(wx.Dialog):
    def __init__(self,parent,id,title, size=(-1,120), pos=wx.DefaultPosition,
            style=wx.DEFAULT_DIALOG_STYLE):
        wx.Dialog.__init__(self,parent,id,title,pos,size,style)
        pnl = wx.Panel(self,-1)
        sizer0 = wx.BoxSizer(wx.VERTICAL)
        sizer0.Add(wx.StaticText(pnl,-1,"\n".join((
                "Apropos gaat nu slapen in de System tray",
                "Er komt een icoontje waarop je kunt klikken om hem weer wakker te maken"
                ))),1,wx.ALL,5)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        self.Check = wx.CheckBox(pnl, -1, "Deze melding niet meer laten zien")
        sizer1.Add(self.Check,0,wx.EXPAND)
        sizer0.Add(sizer1,0,wx.ALIGN_CENTER_HORIZONTAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        self.bOk = wx.Button(pnl,id=wx.ID_OK)
        ## self.bOk.Bind(wx.EVT_BUTTON,self.on_ok)
        sizer1.Add(self.bOk,0,wx.EXPAND | wx.ALL, 2)
        sizer0.Add(sizer1,0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL,5)
        pnl.SetSizer(sizer0)
        pnl.SetAutoLayout(True)
        sizer0.Fit(pnl)
        sizer0.SetSizeHints(pnl)
        pnl.Layout()

class MainFrame(wx.Frame,Apomixin):
    def __init__(self,parent,id):
        wx.Frame.__init__(self,parent,id,"Apropos",pos=(10,10),size=(650,400))
        self.Bind(wx.EVT_CLOSE, self.afsl)
        self.apoicon = wx.Icon(os.path.join(HERE,"apropos.ico"),wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.apoicon)
        pnl = wx.Panel(self,-1)
        self.nb = wx.Notebook(pnl,-1)
        self.nb.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.page_changed)
        self.nb.Bind(wx.EVT_LEFT_DCLICK, self.onLeftDblClick)
        self.nb.Bind(wx.EVT_MIDDLE_DOWN, self.onLeftDblClick)
        self.nb.Bind(wx.EVT_KEY_DOWN, self.on_key)
        self.initapp()
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
                self.nb.AdvanceSelection(False)
            elif keycode == wx.WXK_RIGHT or keycode == wx.WXK_NUMPAD_RIGHT: #  keycode == 316
                self.nb.AdvanceSelection()
            elif keycode == ord("L"): # 76: Ctrl-L reload tabs
                self.nb.DeleteAllPages()
                self.initapp()
                wx.MessageBox("(Re)loaded")
            elif keycode == ord("N"): # 78: Ctrl-N nieuwe tab
                self.newtab()
            elif keycode == ord("W"): # 87: Ctrl-W tab sluiten
                self.closetab()
                skip = False
            elif keycode == ord("H"): # 72: Ctrl-H Hide/minimize
                if self.opts["AskBeforeHide"]:
                    dlg = CheckDialog(self,-1,'Apropos')
                    ## ,                    style = wx.DEFAULT_DIALOG_STYLE | wx.OK | wx.ICON_INFORMATION)
                    dlg.ShowModal()
                    if dlg.Check.GetValue():
                        self.opts["AskBeforeHide"] = False
                    dlg.Destroy()
                self.tbi = wx.TaskBarIcon()
                self.tbi.SetIcon(self.apoicon,"Click to revive Apropos")
                wx.EVT_TASKBAR_LEFT_UP(self.tbi, self.revive)
                wx.EVT_TASKBAR_RIGHT_UP(self.tbi, self.revive)
                self.Hide()
                ## pass # nog uitzoeken hoe
            elif keycode == ord("S"): # 83: Ctrl-S saven zonder afsluiten
                self.afsl()
                wx.MessageBox("Saved")
            elif keycode == ord("Q"): # 81: Ctrl-Q afsluiten na saven
                self.afsl()
                self.Destroy()
        elif keycode == wx.WXK_F1:
            self.helppage()
        elif keycode == wx.WXK_F2:
            self.asktitle()
        elif keycode == wx.WXK_ESCAPE:
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

    def initapp(self):
        self.opts = {"AskBeforeHide":True,"ActiveTab":0}
        self.load_notes()
        if self.apodata:
            for i,x in self.apodata.items():
                if i == 0 and "AskBeforeHide" in x:
                    for key,val in x.items():
                        self.opts[key] = val
                else:
                    self.newtab(titel=x[0],note=x[1])
            self.nb.ChangeSelection(self.opts["ActiveTab"])
        else:
            self.newtab()
            self.current = 0

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

    def revive(self,event=None):
        self.Show()
        self.tbi.Destroy()

    def afsl(self,event=None):
        self.opts["ActiveTab"] = self.nb.GetSelection()
        self.apodata = {0: self.opts}
        for i in range(self.nb.GetPageCount()):
            page = self.nb.GetPage(i)
            title = self.nb.GetPageText(i)
            text = page.txt.GetValue()
            self.apodata[i+1] = (title,text)
        self.save_notes()
        if event:
            event.Skip()

    def helppage(self):
        info = [
            "Apropos door Albert Visser",
            "Om je apropos terug te kunnen vinden",
            "als je de draad even kwijt bent",
            "",
            "Ctrl-N         - nieuwe tab",
            "Ctrl-rechts  - volgende tab",
            "Ctrl-links     - vorige tab",
            "Ctrl-W         - sluit tab",
            "Ctrl-S          - alles opslaan",
            "Ctrl-L          - alles opnieuw laden",
            "Ctrl-Q, Esc - opslaan en sluiten",
            "Ctrl-H         - verbergen in system tray",
            "",
            "F1            - deze (help)informatie",
            "F2            - wijzig tab titel",
            ]
        dlg = wx.MessageDialog(self, "\n".join(info),'Apropos',
            wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

    def asktitle(self):
        dlg = wx.TextEntryDialog(self, 'Nieuwe titel voor de huidige tab:',
                'Apropos', self.nb.GetPageText(self.current))
        if dlg.ShowModal() == wx.ID_OK:
            self.nb.SetPageText(self.current,dlg.GetValue())
        dlg.Destroy()

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
