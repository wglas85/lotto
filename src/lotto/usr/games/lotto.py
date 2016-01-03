#!/usr/bin/python3

'''
Created on 01.05.2015

@author: kinders
'''

import sys
import os

dire = os.path.dirname(__file__)
dire = os.path.dirname(dire)
dire = os.path.join(dire,"lib")
dire = os.path.join(dire,"lotto")
if dire not in sys.path:
    sys.path.append(dire)
del dire

import dialogs  # @UnresolvedImport
from RandomGenerator import RandomGenerator  # @UnresolvedImport
from configparser import ConfigParser
from gi.repository import Gtk
from gi.repository import Gdk
import datetime
import pickle
from copy import deepcopy


class Lotto:
    def __init__(self,editables=None,tips=1,state=None,vs=None):
        if editables is None:
            self.editables = [False for i in range(tips)]  # @UnusedVariable
        else:
            self.editables = editables
        self.tips = tips
        if state is None:
            self.state =  [([False for i in range(45)] if self.editables[j] else [None for i in range(45)]) for j in range(tips)]  # @UnusedVariable
        else:
            self.state = state
        if vs is None:
            self.vs = [[None,None,None,None,None,None,None] for i in range(tips)]  # @UnusedVariable
        else:
            self.vs = vs

class LottoWidget(Gtk.Grid):
    def __init__(self,state=None,editable=True,zs=None):
        if zs is None:
            self.zs = [None,None,None,None,None,None,None]
        else:
            self.zs = zs
        
        self.editable = editable
        
        if state==None:
            self.state =  [False for i in range(0,45)] if editable else [None for i in range(0,45)]  # @UnusedVariable
        else:
            self.state = state
        
        Gtk.Grid.__init__(self,hexpand=True,vexpand=True)
        
        self.buttons = []
        
        for i in range(0,45): # @UnusedVariable
            buttonId = len(self.buttons)
            self.buttons.append(Gtk.Button(label="%d"%(buttonId+1),hexpand=True,vexpand=True))
            
            self.buttons[buttonId].get_style_context().add_class("numberBtn")
            self.buttons[buttonId].set_size_request(80,80)
            self.buttons[buttonId].connect("clicked", self.on_button1_clicked)
            self.attach(self.buttons[buttonId],buttonId%9,buttonId/9,1,1)
    def set_buttons(self):
        for i1,i2 in enumerate(self.state):
            if i2==True:
                self.buttons[i1].set_image(Gtk.Image.new_from_file(os.path.join("/usr/share/lotto/images","crossed.svg" if self.editable else "ok.svg")))
                buttonId = i1
                if buttonId < 9:
                    self.buttons[buttonId].set_label("%d \u2009"%(buttonId+1))
                else:
                    self.buttons[buttonId].set_label("%d"%(buttonId+1))
            elif i2==False and not self.editable:
                self.buttons[i1].set_image(Gtk.Image.new_from_file(os.path.join("/usr/share/lotto/images","crossed.svg")))
                buttonId = i1
                if buttonId < 9:
                    self.buttons[buttonId].set_label("%d \u2009"%(buttonId+1))
                else:
                    self.buttons[buttonId].set_label("%d"%(buttonId+1))
            elif i2=="Zusatzzahl":
                self.buttons[i1].set_image(Gtk.Image.new_from_file(os.path.join("/usr/share/lotto/images","ok2.svg")))
                buttonId = i1
                if buttonId < 9:
                    self.buttons[buttonId].set_label("%d \u2009"%(buttonId+1))
                else:
                    self.buttons[buttonId].set_label("%d"%(buttonId+1))
    
    def on_button1_clicked(self, widget):
        
        buttonId = self.buttons.index(widget)
        
        #print ("on_button1_clicked: %d" % (buttonId+1))
        if self.state[buttonId]==False and self.editable and self.state.count(True)!= 6:
            dirn = "/usr/share/lotto/images"
            fn = os.path.join(dirn,"crossed.svg")

            self.buttons[buttonId].set_image(Gtk.Image.new_from_file(fn))
            if buttonId < 9:
                self.buttons[buttonId].set_label("%d \u2009"%(buttonId+1))
            else:
                self.buttons[buttonId].set_label("%d"%(buttonId+1))
                
            self.state[buttonId] = True
    def ziehung(self,z1,z2,z3,z4,z5,z6,z7):
        #z1 test
        if self.zs[0] is not None:
            z1 = self.zs[0]
        #z2 test
        if self.zs[1] is not None:
            z2 = self.zs[1]
        #z3 test
        if self.zs[2] is not None:
            z3 = self.zs[2]
        #z4 test
        if self.zs[3] is not None:
            z4 = self.zs[3]
        #z5 test
        if self.zs[4] is not None:
            z5 = self.zs[4]
        #z6 test
        if self.zs[5] is not None:
            z6 = self.zs[5]
        #z7 test
        if self.zs[6] is not None:
            z7 = self.zs[6]
        self.zs = [z1,z2,z3,z4,z5,z6,z7]
        
        if self.state.count(True)==6 and self.editable:
            self.editable = False
            
            workstate = deepcopy(self.state)
            
            for i1,i2 in enumerate(self.state):
                if i2==True:
                    workstate[i1] = False
                elif i2==False:
                    workstate[i1] = None
                    
            
            #print("%d,%d,%d,%d,%d,%d,%d"%(z1,z2,z3,z4,z5,z6,z7))
            #z1 = 1
            #z2 = 2
            #z3 = 3
            #z4 = 4
            #z5 = 5
            #z6 = 6
            #z7 = 7
            #Auswertung↓
            if self.state[z1-1]==True:
                z1A = 1
                workstate[z1-1] = True
            else:
                z1A = 0
            if self.state[z2-1]==True:
                z2A = 1
                workstate[z2-1] = True
            else:
                z2A = 0
            if self.state[z3-1]==True:
                z3A = 1
                workstate[z3-1] = True
            else:
                z3A = 0
            if self.state[z4-1]==True:
                z4A = 1
                workstate[z4-1] = True
            else:
                z4A = 0
            if self.state[z5-1]==True:
                z5A = 1
                workstate[z5-1] = True
            else:
                z5A = 0
            if self.state[z6-1]==True:
                z6A = 1
                workstate[z6-1] = True
            else:
                z6A = 0
            zA = z1A+z2A+z3A+z4A+z5A+z6A
            datetimev = datetime.datetime.now().isoformat()
            Zahl_zu_Wort = {0:"null",1:"eins",2:"zwei",3:"drei",4:"vier",5:"fünf",6:"sechs"}
            if self.state[z7-1]==True:
                sys.stdout.write("%ser mit Zusatzzahl\n"%(Zahl_zu_Wort[zA]))
                if zA>2:
                    filename = os.path.expanduser("~/.local/share/lotto/history.txt")
                    f = open(filename, 'a')
                    f.write("%s : %der mit Zusatzzahl\n"%(datetimev,zA))
                    f.close()
                workstate[z7-1] = "Zusatzzahl"
            else:
                sys.stdout.write("%ser\n"%(Zahl_zu_Wort[zA]))
                if zA>2:
                    filename = os.path.expanduser("~/.local/share/lotto/history.txt")
                    f = open(filename, 'a')
                    f.write("%s : %der\n"%(datetimev,zA))
                    f.close()
            #Auswertung↑
            self.state = workstate
            self.set_buttons()
                

class LottoWindow(Gtk.Window):
    
    def __init__(self, lotto=None, tips=None, file=None):
        
        self.file = file
        
        self.config = ConfigParser()
        self.config.read(os.path.expanduser("~/.local/share/lotto/preferences.ini"))
        if tips == None:
            tips = self.config.getint("tips", "tips")
        if lotto == None:
            self.lotto = Lotto([True for i in range(tips)], tips)  # @UnusedVariable
        else:
            self.lotto = lotto
            
        
        self.closed = False
        
        #self.state = [None for i in range(0,45)]
        #print(len(self.state))
        
        Gtk.Window.__init__(self, title="Lotto")
        
        self.connect("key-press-event",self.on_key_press)
        
        self.set_icon_from_file("/usr/share/icons/hicolor/scalable/apps/lotto.svg")
        
        self.headerbar = Gtk.HeaderBar()
        self.headerbar.set_title("lotto")
        
        self.menuitems = {"ziehung":self.ziehung,
                          "Gewinne":self.on_Button_clicked,
                          "löschen":self.on_realoadButton_clicked,
                          "einstellungen":self.on_preferences_clicked,
                          "speichern":self.on_save_clicked,
                          "öffnen":self.on_open_clicked,
                          "speichern als":self.on_save_as_clicked,
                          "tipps":{i+1:self.on_tipp_clicked for i in range(self.lotto.tips)}}
        
        self.menubutton = Gtk.MenuButton()
        self.load_menu()
        
        self.headerbar.pack_end(self.menubutton)
            
        self.headerbar.set_show_close_button(True)
        self.set_titlebar(self.headerbar)
        
        self.notebook = Gtk.Notebook()
        self.lottowidgets = []
        for i in range(self.lotto.tips):
            self.lottowidgets.append(LottoWidget(self.lotto.state[i], self.lotto.editables[i],self.lotto.vs[i]))
            self.notebook.append_page(child=self.lottowidgets[i],tab_label=Gtk.Label(label="tipp %s"%(i+1)))
        self.set_buttons()
        
        self.notebook.set_scrollable(True)
        
        self.add(self.notebook)
    def go_to_tipp(self,tipp):
        self.notebook.set_current_page(tipp-1)
    def on_tipp_clicked(self,target):
        tipp = int(target.get_label())
        self.go_to_tipp(tipp)
    def on_key_press(self,target,event):
        mod = Gtk.accelerator_get_label(event.keyval,event.state)
        #name = Gdk.keyval_name(event.keyval)
        if mod=="Strg+S":
            self.save()
        elif mod=="Umschalt+Strg+S":
            self.save_as()
    def on_open_clicked(self,target):
        self.open()
    def open(self):
        dialog = Gtk.FileChooserDialog("Please choose a file", self,
            Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            try:
                self.file = dialog.get_filename()
                newlotto = pickle.load(open(dialog.get_filename(),"rb"))
            except:
                pass
            else:
                if type(newlotto)==Lotto:
                    self.lotto = newlotto
                    self.remove(self.notebook)
                    self.notebook = Gtk.Notebook()
                    self.lottowidgets = []
                    for i in range(self.lotto.tips):
                        self.lottowidgets.append(LottoWidget(self.lotto.state[i], self.lotto.editables[i],self.lotto.vs[i]))
                        self.notebook.append_page(child=self.lottowidgets[i],tab_label=Gtk.Label(label="tipp %s"%(i+1)))
                    self.set_buttons()
                    self.add(self.notebook)
                    self.notebook.show_all()
                    self.show_all()
        dialog.destroy()
    def save(self):
        if self.file==None:
            self.save_as()
        else:
            fp = open(self.file,"wb")
            pickle.dump(Lotto([i.editable for i in self.lottowidgets], self.lotto.tips, [i.state for i in self.lottowidgets],[i.zs for i in self.lottowidgets]),fp)
            fp.close()
    def save_as(self):
        dialog1 = Gtk.FileChooserDialog("Please choose a file", self,
            Gtk.FileChooserAction.SAVE,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_SAVE, Gtk.ResponseType.OK))
        
        response1 = dialog1.run()
        filename = dialog1.get_filename()
        dialog1.destroy()
        if response1 == Gtk.ResponseType.OK:
            if os.path.exists(filename):
                dialog2 = Gtk.MessageDialog(self,
                                            Gtk.DialogFlags.USE_HEADER_BAR,
                                            Gtk.MessageType.QUESTION,
                                            Gtk.ButtonsType.YES_NO,
                                            text="diese Datei existiert bereits wollen sie sie überschreiben")
                response2 = dialog2.run()
                dialog2.destroy()
                if response2==-9:
                    return
            fp = open(filename,"wb" if os.path.exists(filename) else "xb")
            pickle.dump(Lotto([i.editable for i in self.lottowidgets], self.lotto.tips, [i.state for i in self.lottowidgets],[i.zs for i in self.lottowidgets]),fp)
            fp.close()
    def on_save_as_clicked(self,target):
        self.save_as()
    def on_save_clicked(self,target):
        self.save()
    def on_Button_clicked(self, event):
        dialog = dialogs.winningsdialog(self)
        dialog.run()
        dialog.destroy()
   
    def set_buttons(self):
        for i in self.lottowidgets:
            i.set_buttons()
            
    def ziehung(self,*args,**kwargs):
        rg = RandomGenerator()
        zs = (rg.nextNumber(45), rg.nextNumber(45), rg.nextNumber(45), rg.nextNumber(45), rg.nextNumber(45), rg.nextNumber(45), rg.nextNumber(45))
        for i in self.lottowidgets:
            i.ziehung(*zs)
        rg.finalize()
    def load_menu(self):
        def get_menu_from_dict(vdict):
            menu = Gtk.Menu()
            for i in sorted(vdict.keys()):
                item = Gtk.MenuItem(label=str(i))
                menu.append(item)
                vx = vdict[i]
                if isinstance(vx, dict):
                    item.set_submenu(get_menu_from_dict(vx))
                else:
                    item.connect("activate",vx)
            menu.show_all()
            return menu
        self.menu = get_menu_from_dict(self.menuitems)
        self.menubutton.set_popup(self.menu)
    def my_remove(self):
        tips = self.config.getint("tips", "tips")
        self.lotto = Lotto([True for i in range(tips)], tips)  # @UnusedVariable
        self.remove(self.notebook)
        self.notebook = Gtk.Notebook()
        self.lottowidgets = []
        self.menuitems["tipps"] = {i+1:self.on_tipp_clicked for i in range(self.lotto.tips)}
        self.load_menu()
        for i in range(self.lotto.tips):
            self.lottowidgets.append(LottoWidget(self.lotto.state[i], self.lotto.editables[i]))
            self.notebook.append_page(child=self.lottowidgets[i],tab_label=Gtk.Label(label="tipp %s"%(i+1)))
        self.set_buttons()
        self.add(self.notebook)
        self.show_all()
    def on_realoadButton_clicked(self,event):
        self.my_remove()
    def on_preferences_clicked(self,event):
        dialog = dialogs.preferencesdialog(self)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.config.set("tips", "tips", str(dialog.tips))
            fp = open(os.path.expanduser("~/.local/share/lotto/preferences.ini"),"w")
            self.config.write(fp)
            fp.close()
        dialog.destroy()
    def closedf(self,*a):
        self.config.clear()
        self.closed = True

class window1(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Gewinne")
        self.grid = Gtk.Grid()
        self.Label1 = Gtk.Label(label="Gewinne:")
        filename = os.path.expanduser("~/.local/share/lotto/history.txt")
        f = open(filename, 'r')
        gewinne = len(f.readlines())
        self.Label2 = Gtk.Label(label="%d         "%(gewinne))
        f.close()
        self.grid.attach(self.Label2,2,1,1,1)
        self.grid.attach(self.Label1,1,1,1,1)
        self.add(self.grid)
    

if __name__ == '__main__':
    '''
    win = window2()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()
    '''
    if len(sys.argv)==1:
        cssProvider = Gtk.CssProvider()
        cssProvider.load_from_path("/usr/share/lotto/styles/Lotto.css")
        screen = Gdk.Screen.get_default()
        styleContext = Gtk.StyleContext()
        styleContext.add_provider_for_screen(screen, cssProvider,
                                             Gtk.STYLE_PROVIDER_PRIORITY_USER)

        win = LottoWindow()
        win.connect("destroy", Gtk.main_quit)
        win.connect("destroy", win.closedf)
        win.show_all()
        Gtk.main()
    else:
        tips = None
        file = None
        for i1,i2 in enumerate(sys.argv):
            if i2=="--":
                break
            elif i2 == "--tips":
                try:
                    tips = sys.argv[i1+1]
                except IndexError:
                    sys.stderr.write("""lotto: Die Option »--tips« erfordert ein Argument
„lotto --help“ liefert weitere Informationen.""")
            elif i2.startswith("--tips="):
                if i2[7:].isdigit():
                    tips = int(i2[7:])
            else:
                file = os.path.abspath(i2)
        try:
            file = os.path.abspath(sys.argv[i1+1])
        except IndexError:
            pass
        cssProvider = Gtk.CssProvider()
        cssProvider.load_from_path(os.path.join("/usr/share/lotto/styles","Lotto.css"))
        screen = Gdk.Screen.get_default()
        styleContext = Gtk.StyleContext()
        styleContext.add_provider_for_screen(screen, cssProvider,
                                             Gtk.STYLE_PROVIDER_PRIORITY_USER)
        
        
        if file==None:
            win = LottoWindow(tips=tips)
        else:
            win = LottoWindow(lotto=pickle.load(open(file,"rb")),file=file)
        win.connect("destroy", Gtk.main_quit)
        win.connect("destroy", win.closedf)
        win.show_all()
        Gtk.main()
