import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from yt_lib import yt_install

class MyWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Youtube Installation")

        main_box = Gtk.HBox()
        self.add(main_box)

        self.button = Gtk.Button(label=" Install ")
        #self.button.connect("clicked", self.on_button_clicked)
        self.button.connect("clicked", self.install_one_song) 
        main_box.pack_start(self.button,1,1,10)

        self.url_entry = Gtk.Entry()
        self.url_entry.set_placeholder_text("Paste Url Here")
        main_box.pack_start(self.url_entry,1,1,10)

    def install_one_song(self,widget):
        print(self.url_entry.get_text())


    def on_button_clicked(self, widget):
        link_list = yt_install.set_link_list()
        line = yt_install.loop(link_list)
        print("installation compleated.",line," sound downloaded")

win = MyWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()



#first try
