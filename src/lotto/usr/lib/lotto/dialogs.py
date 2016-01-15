'''
Created on 15.12.2015

@author: michi
'''
from configparser import ConfigParser
from gi.repository import Gtk
import os

class preferencesdialog(Gtk.Dialog):
    def __init__(self,parent):
        self.tips_changed = False
        self.config = ConfigParser()
        filename = os.path.expanduser("~/.local/share/lotto/preferences.ini")
        self.config.read(filename)
        
        self.parent = parent
        Gtk.Dialog.__init__(self, "einstellungen", parent, 0,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_CLOSE, Gtk.ResponseType.OK))
        
        self.set_resizable(False)
        
        self.tips = self.config.getint("tips", "tips")
        
        self.notebook = Gtk.Notebook()
        self.notebookpages = [(Gtk.Entry(text=self.tips),Gtk.Label(label="tips"))]
        for child,tab_label in self.notebookpages:
            self.notebook.append_page(child=child,tab_label=tab_label)
        self.notebookpages[0][0].connect("notify::text",self.on_tips_changed)
        box = self.get_content_area()
        box.add(self.notebook)
        self.show_all()
    def on_tips_changed(self,target,params):
        try:
            self.tips = int(target.get_text())
        except:
            pass
class winningsdialog(Gtk.Dialog):
    def __init__(self,parent):
        Gtk.Dialog.__init__(self, "Gewinne", parent, 0,
            (Gtk.STOCK_OK, Gtk.ResponseType.OK))
        self.grid = Gtk.Grid()
        self.Label1 = Gtk.Label(label="Gewinne:")
        filename = os.path.expanduser("~/.local/share/lotto/history.txt")
        f = open(filename, 'r')
        gewinne = len(f.readlines())
        self.Label2 = Gtk.Label(label="%d         "%(gewinne))
        f.close()
        self.grid.attach(self.Label2,2,1,1,1)
        self.grid.attach(self.Label1,1,1,1,1)
        box = self.get_content_area()
        box.add(self.grid)
        self.show_all()
