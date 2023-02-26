
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class MainWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="window title")
        main_box = Gtk.VBox()
        self.add(main_box)

    def close(self):
        pass
