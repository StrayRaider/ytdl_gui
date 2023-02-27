import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class Playlist(Gtk.VBox):
    def __init__(self,parent):
        Gtk.VBox.__init__(self)
        self.parent = parent
        self.label = Gtk.Label("playlist")
        self.pack_start(self.label,0,0,5)
        
        self.download_button = Gtk.Button()
        self.download_button.set_label("Download")
        self.download_button.connect("clicked",self.download_button_clicked)
        self.pack_start(self.download_button,0,0,5)
        
    def download_button_clicked(self,widget):
        self.parent.stack.set_visible_child_name("download")
