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
from gi.repository import Gtk, GObject
from gi.repository import Gdk
import time
import pickle
from copy import deepcopy


class Lotto:
    def __init__(self,tipps=[]):
        self.tipps = tipps
    def get_n_tipps(self):
        return len(self.tipps)
    def clear(self):
        self.tipps.clear()
    def clear_all_tipps(self):
        for i in self.tipps:
            i.clear()
    def get_nth_tipp(self,tipp):
        return self.tipps[tipp]
    def append(self,tipp):
        self.tipps.append(tipp)
        

class Tipp:
    def __init__(self,editable=None,state=None):
        if editable is None:
            self.editable = True
        else:
            self.editable = editable
        if state is None:
            self.state =  45 * [False] if self.editable else 45 * [None]  # @UnusedVariable
        else:
            self.state = state
    def clear(self):
        self.editable = True
        self.state =  45 * [False]
        

class TippWidget(Gtk.Grid):
    def __init__(self,tipp=Tipp()):
        self.tipp = tipp
        
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
        for i1,i2 in enumerate(self.tipp.state):
            if i2==True:
                self.buttons[i1].set_image(Gtk.Image.new_from_file(os.path.join("/usr/share/lotto/images","crossed.svg" if self.tipp.editable else "ok.svg")))
                buttonId = i1
                if buttonId < 9:
                    self.buttons[buttonId].set_label("%d \u2009"%(buttonId+1))
                else:
                    self.buttons[buttonId].set_label("%d"%(buttonId+1))
            elif i2==False:
                if self.tipp.editable:
                    self.buttons[i1].props.image = None
                    buttonId = i1
                    self.buttons[buttonId].set_label("%d"%(buttonId+1))
                else:
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
        self.show_all()
    def clear(self):
        self.tipp.clear()
        self.set_buttons()
    def on_button1_clicked(self, widget):
        
        buttonId = self.buttons.index(widget)
        
        #print ("on_button1_clicked: %d" % (buttonId+1))
        if self.tipp.state[buttonId]==False and self.tipp.editable and self.tipp.state.count(True)!= 6:
            dirn = "/usr/share/lotto/images"
            fn = os.path.join(dirn,"crossed.svg")

            self.buttons[buttonId].set_image(Gtk.Image.new_from_file(fn))
            if buttonId < 9:
                self.buttons[buttonId].set_label("%d \u2009"%(buttonId+1))
            else:
                self.buttons[buttonId].set_label("%d"%(buttonId+1))
                
            self.tipp.state[buttonId] = True
    def ziehung(self,z1,z2,z3,z4,z5,z6,z7):
        
        if self.tipp.state.count(True)==6 and self.tipp.editable:
            newstate = []
            
            numbers = 0
            Zusatzzahl = False
            for i1,i2 in enumerate(self.tipp.state):
                if i2==True:
                    if i1==z1 or i1==z2 or i1==z3 or i1==z4 or i1==z5 or i1==z6:
                        numbers += 1
                        newstate.append(True)
                    elif i1==z7:
                        Zusatzzahl = True
                        newstate.append("Zusatzzahl")
                    else:
                        newstate.append(False)
                elif i2==False:
                    newstate.append(None)
            datetime = time.strftime("%d.%B %Y, %H:%M")
            if Zusatzzahl:
                sys.stdout.write("%ser mit Zusatzzahl\n"%(numbers))
                if numbers>2:
                    filename = os.path.expanduser("~/.local/share/lotto/history.txt")
                    f = open(filename, 'a')
                    f.write("%s : %der mit Zusatzzahl\n"%(datetime,numbers))
                    f.close()
                newstate[z7] = "Zusatzzahl"
            else:
                sys.stdout.write("%ser\n"%(numbers))
                if numbers>2:
                    filename = os.path.expanduser("~/.local/share/lotto/history.txt")
                    f = open(filename, 'a')
                    f.write("%s : %der\n"%(datetime,numbers))
                    f.close()
            #Auswertung↑
            self.tipp.state = newstate
            self.tipp.editable = False
            self.set_buttons()
                

class LottoWidget(Gtk.Notebook):
    
    def __init__(self, lotto=None, tipps=None, file=None):
        
        self.file = file
        
        self.config = ConfigParser()
        self.config.read(os.path.expanduser("~/.local/share/lotto/preferences.ini"))
        if tipps == None:
            tipps = self.config.getint("tipps", "tipps")
        if lotto == None:
            self.lotto = Lotto([Tipp() for i in range(tipps)])  # @UnusedVariable
        else:
            self.lotto = lotto
            
        Gtk.Notebook.__init__(self)
        self.set_scrollable(True)
        
        GObject.type_register(LottoWidget)
        GObject.signal_new("reaload",LottoWidget,GObject.SIGNAL_RUN_FIRST,
                   GObject.TYPE_NONE, [])
        
        self.tippwidgets = []
        for i in range(self.lotto.get_n_tipps()):
            self.tippwidgets.append(TippWidget(self.lotto.get_nth_tipp(i)))
            self.append_page(child=self.tippwidgets[i],tab_label=Gtk.Label(label="tipp %s"%(i+1)))
        self.set_buttons()
    def go_to_tipp(self,tipp):
        self.set_current_page(tipp-1)
    
    def open(self):
        dialog = Gtk.FileChooserDialog("Please choose a file", self.get_tooltip_window(),
            Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            try:
                self.file = dialog.get_filename()
                newlotto = pickle.load(open(dialog.get_filename(),"rb"))
            except pickle.PickleError:
                pass
            else:
                if isinstance(newlotto, Lotto):
                    for i in range(self.get_n_pages()):
                        self.remove_page(0)
                    self.lotto = newlotto
                    self.tippwidgets = []
                    for i in range(self.lotto.get_n_tipps()):
                        self.tippwidgets.append(TippWidget(self.lotto.tipps[i]))
                        self.append_page(child=self.tippwidgets[i],tab_label=Gtk.Label(label="tipp %s"%(i+1)))
                    self.set_buttons()
                    self.show_all()
        dialog.destroy()
    def save(self):
        if self.file==None:
            self.save_as()
        else:
            fp = open(self.file,"wb")
            pickle.dump(Lotto(),fp)
            fp.close()
    def save_as(self):
        dialog1 = Gtk.FileChooserDialog("Please choose a file", self.get_tooltip_window(),
            Gtk.FileChooserAction.SAVE,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_SAVE, Gtk.ResponseType.OK))
        while True:
            response1 = dialog1.run()
            filename = dialog1.get_filename()
            if response1 == Gtk.ResponseType.OK:
                if os.path.exists(filename):
                    dialog2 = Gtk.MessageDialog(self.get_tooltip_window(),
                                                Gtk.DialogFlags.USE_HEADER_BAR,
                                                Gtk.MessageType.QUESTION,
                                                Gtk.ButtonsType.YES_NO,
                                                text="diese Datei existiert bereits, wollen sie sie überschreiben")
                    response2 = dialog2.run()
                    dialog2.destroy()
                    if response2==-9:
                        continue
                fp = open(filename,"wb" if os.path.exists(filename) else "xb")
                pickle.dump(Lotto([i.tipp for i in self.tippwidgets]),fp)
                fp.close()
                break
            else:
                break
        dialog1.destroy()
    
    def wins(self):
        dialog = dialogs.winningsdialog(self.get_tooltip_window())
        dialog.run()
        dialog.destroy()
   
    def set_buttons(self):
        for i in self.tippwidgets:
            i.set_buttons()
            
    def ziehung(self):
        rg = RandomGenerator()
        zs = (rg.nextNumber(45), rg.nextNumber(45), rg.nextNumber(45), rg.nextNumber(45), rg.nextNumber(45), rg.nextNumber(45), rg.nextNumber(45))
        print(zs)
        for i in self.tippwidgets:
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
    def clear(self):
        for i in self.tippwidgets:
            i.clear()
    def reaload(self):
        tipps = self.config.getint("tipps", "tipps")
        
        
        len_tippwidgets = len(self.tippwidgets)
        if len_tippwidgets>tipps:
            self.tippwidgets = self.tippwidgets[:tipps]
            self.lotto.tipps = self.lotto.tipps[:tipps]
            for i in range(len_tippwidgets-tipps):
                self.remove_page(tipps)
        elif len_tippwidgets<tipps:
            for i in range(tipps-len_tippwidgets):
                i2 = len_tippwidgets+i
                self.lotto.append(Tipp())
                self.tippwidgets.append(TippWidget(self.lotto.get_nth_tipp(i2)))
                self.append_page(child=self.tippwidgets[i2],tab_label=Gtk.Label(label="tipp %s"%(i2+1)))
        self.set_buttons()
        self.show_all()
        self.emit("reaload")
    def preferences(self):
        dialog = dialogs.preferencesdialog(self.get_tooltip_window())
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.config.set("tipps", "tipps", str(dialog.tipps))
            fp = open(os.path.expanduser("~/.local/share/lotto/preferences.ini"),"w")
            self.config.write(fp)
            fp.close()
            self.reaload()
        dialog.destroy()
    

class LottoWindow(Gtk.Window):
    def __init__(self,*args,**kwargs):
        Gtk.Window.__init__(self,title="lotto")
        
        self.connect("key-press-event",self.on_key_press)
        
        self.set_icon_from_file("/usr/share/icons/hicolor/scalable/apps/lotto.svg")
        
        
        
        self.lottowidget = LottoWidget(*args,**kwargs)
        self.lottowidget.connect("reaload",self.on_reaload)
        
        self.headerbar = Gtk.HeaderBar()
        self.headerbar.set_title("lotto")
        
        self.menuitems = {"ziehung":self.on_ziehung_clicked,
                          "Gewinne":self.on_wins_clicked,
                          "löschen":self.on_remove_clicked,
                          "einstellungen":self.on_preferences_clicked,
                          "speichern":self.on_save_clicked,
                          "öffnen":self.on_open_clicked,
                          "speichern als":self.on_save_as_clicked,
                          "tipps":{i+1:self.on_tipp_clicked for i in range(self.lottowidget.lotto.get_n_tipps())}}
        
        self.menubutton = Gtk.MenuButton()
        self.load_menu()
        
        self.headerbar.pack_end(self.menubutton)
            
        self.headerbar.set_show_close_button(True)
        self.set_titlebar(self.headerbar)
        
        self.add(self.lottowidget)
    
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
        self.show_all()
    def on_remove_clicked(self,x):
        self.lottowidget.clear()
    def on_save_as_clicked(self,x):
        self.lottowidget.save_as()
    def on_save_clicked(self,x):
        self.lottowidget.save()
    def on_wins_clicked(self,x):
        self.lottowidget.wins()
    def on_preferences_clicked(self,x):
        self.lottowidget.preferences()
    def on_tipp_clicked(self,target):
        tipp = int(target.get_label())
        self.lottowidget.go_to_tipp(tipp)
    def on_key_press(self,target,event):
        mod = Gtk.accelerator_get_label(event.keyval,event.state)
        #name = Gdk.keyval_name(event.keyval)
        if mod=="Strg+S":
            self.save()
        elif mod=="Umschalt+Strg+S":
            self.save_as()
    def on_open_clicked(self,x):
        self.lottowidget.open()
    
    def on_ziehung_clicked(self,event):
        self.lottowidget.ziehung()
    def on_reaload(self,target):
        self.menuitems["tipps"] = {i+1:self.on_tipp_clicked for i in range(self.lottowidget.lotto.get_n_tipps())}
        self.load_menu()

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
        win.show_all()
        Gtk.main()
    else:
        tipps = None
        file = None
        for i1,i2 in enumerate(sys.argv):
            if i2=="--":
                break
            elif i2 == "--tipps":
                try:
                    tipps = sys.argv[i1+1]
                except IndexError:
                    sys.stderr.write("""lotto: Die Option »--tipps« erfordert ein Argument
„lotto --help“ liefert weitere Informationen.""")
            elif i2.startswith("--tipps="):
                if i2[7:].isdigit():
                    tipps = int(i2[7:])
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
            win = LottoWindow(tipps=tipps)
        else:
            win = LottoWindow(lotto=pickle.load(open(file,"rb")),file=file)
        win.connect("destroy", Gtk.main_quit)
        win.show_all()
        Gtk.main()
