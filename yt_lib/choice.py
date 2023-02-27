import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class Choice(Gtk.VBox):
    def __init__(self,parent):
        Gtk.VBox.__init__(self)
        self.parent = parent
        self.label = Gtk.Label("choice")
        self.pack_start(self.label,0,0,5)
        
        self.download_video_button = Gtk.Button()
        self.download_video_button.set_label("video indir")
        self.download_video_button.connect("clicked",self.video_button_clicked)
        self.download_playlist_button = Gtk.Button()
        self.download_playlist_button.set_label("playlist indir")
        self.download_playlist_button.connect("clicked",self.playlist_button_clicked)
        self.pack_start(self.download_video_button,0,0,5)
        self.pack_start(self.download_playlist_button,0,0,5)
        
    def video_button_clicked(self,widget):
        self.parent.stack.set_visible_child_name("sd")
    
    def playlist_button_clicked(self,widget):
        self.parent.stack.set_visible_child_name("playlist")
