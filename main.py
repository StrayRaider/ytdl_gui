import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from yt_lib import yt_install

import threading

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

        new_box = Gtk.HBox()
        install_box.pack_start(new_box,0,0,10)
        self.url_entry = Gtk.Entry()
        self.url_entry.set_placeholder_text("Paste Url Here")
        new_box.pack_start(self.url_entry,0,0,10)

        new_box = Gtk.HBox()
        install_box.pack_start(new_box,0,0,10)
        self.dir_entry = Gtk.Entry()
        self.dir_entry.set_placeholder_text("directory")
        new_box.pack_start(self.dir_entry,0,0,10)

        but_box = Gtk.HBox()
        install_box.pack_start(but_box,0,0,10)

        new_box = Gtk.HBox()
        but_box.pack_start(new_box,0,0,10)
        self.button = Gtk.Button(label=" Install ")
        #self.button.connect("clicked", self.on_button_clicked)
        self.button.connect("clicked", self.install_one_song) 
        new_box.pack_start(self.button,0,0,10)

        #new_box = Gtk.HBox()
        #but_box.pack_start(new_box,0,0,10)
        #self.button = Gtk.Button(label=" Add into list ")
        #self.button.connect("clicked", self.on_button_clicked)
        #self.button.connect("clicked", yt_install.add_url_to_list) 
        #new_box.pack_start(self.button,0,0,10)

    def settings_but_clicked(self,widget):
        pass

    def install_one_song(self,widget):
        self.entered_url = self.url_entry.get_text()
        print(self.entered_url)
        if self.entered_url != "":
            new_dir = self.dir_entry.get_text()
            print("ok")
            if new_dir != "":
                yt_install.set_dir(str(new_dir))
            print("ok")
            #yt_install.download(self.entered_url) 
            install_thread = threading.Thread(target = yt_install.download, args = [self.entered_url])
            print("installation done")
            install_thread.start()

    def on_button_clicked(self, widget):
        link_list = yt_install.set_link_list()
        line = yt_install.loop(link_list)
        print("installation compleated.",line," sound downloaded")

def quit_app(arg):
    #global install_thread
    print("quiting..")
    #print(type(install_thread))
    Gtk.main_quit()
    print("Done")

#if not t1.isAlive(): is thread alive

win = MyWindow()
win.connect("destroy", quit_app)
win.show_all()
Gtk.main()