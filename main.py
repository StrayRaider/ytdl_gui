import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from yt_lib import yt_install

class MyWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Youtube Installation")

        main_box = Gtk.VBox()
        self.add(main_box)

        top_box = Gtk.HBox()
        main_box.pack_start(top_box,0,0,10)
        self.settings_button = Gtk.Button(label = "Settings")
        self.settings_button.connect("clicked", self.settings_but_clicked)
        top_box.pack_start(self.settings_button,0,0,10)


        install_box = Gtk.VBox()
        #install_box.set_size_request(width=400, height=250)  
        main_box.pack_start(install_box,0,0,10)

        self.url_entry = Gtk.Entry()
        self.url_entry.set_placeholder_text("Paste Url Here")
        install_box.pack_start(self.url_entry,0,0,10)

        self.dir_entry = Gtk.Entry()
        self.dir_entry.set_placeholder_text("directory")
        install_box.pack_start(self.dir_entry,0,0,10)

        self.button = Gtk.Button(label=" Install ")
        #self.button.connect("clicked", self.on_button_clicked)
        self.button.connect("clicked", self.install_one_song) 
        install_box.pack_start(self.button,0,0,10)

    def settings_but_clicked(self,widget):
        pass

    def install_one_song(self,widget):
        self.entered_url = self.url_entry.get_text()
        print(self.entered_url)

    def on_button_clicked(self, widget):
        link_list = yt_install.set_link_list()
        line = yt_install.loop(link_list)
        print("installation compleated.",line," sound downloaded")

win = MyWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()



#first try
