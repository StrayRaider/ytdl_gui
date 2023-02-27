import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from yt_lib import yt_install, settings_win, choice, playlist, download, search_download

import threading

class MyWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Youtube Installation")

        self.stack = Gtk.Stack()
        self.add(self.stack)
        self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        self.stack.set_transition_duration(1000)
        self.stack.add_titled(choice.Choice(self),"choice","choice_screen")
        self.stack.add_titled(playlist.Playlist(self),"playlist","choice_screen")
        self.stack.add_titled(search_download.Sd(self),"sd","choice_screen")
        self.stack.add_titled(download.Download(self),"download","choice_screen")
        
"""
    def add_song(self,widget):
        self.iSongStore.append([self.title_entry.get_text(), True, self.url_entry.get_text(),False])

    def del_tree_obj(self, widget, path, column, which):
        print(path, column)
        if which == "s":
            iter = self.sSongStore.get_iter(path)
            self.sSongStore.remove(iter)
        elif which == "i":
            iter = self.iSongStore.get_iter(path)
            self.iSongStore.remove(iter)

    def addToStore(self, obj_list, store, is_tick,del_b):
        for obj in obj_list:
            store.append([obj[0],is_tick, obj[1],del_b])

    def tree_but_toggle(self, widget, path, column, old_ls):
        #basılmadan önceki hali
        #print(self.sSongStore[path][column])#true ya da false döner
        if old_ls == "s":
            self.sSongStore[path][column] = not self.sSongStore[path][column]
            self.add_into_install(path)
        if old_ls == "i":
            self.iSongStore[path][column] = not self.iSongStore[path][column]
            self.add_into_search(path)

    def add_into_install(self, path, widget = None):
        self.iSongStore.append([*self.sSongStore[path]])
        iter = self.sSongStore.get_iter(path)
        self.sSongStore.remove(iter)

    def add_into_search(self, path, widget = None):
        self.sSongStore.append([*self.iSongStore[path]])
        iter = self.iSongStore.get_iter(path)
        self.iSongStore.remove(iter)

    def search(self, widget):
        search_count = self.song_count_b.get_value_as_int()
        entry = self.search_entry.get_text()
        search_thread = threading.Thread(target =yt_install.search, args = [entry])
        search_thread.start()
        yt_install.search(entry,search_count)
        self.s_song_list = yt_install.song_list
        self.addToStore(self.s_song_list,self.sSongStore, False, False)

    def settings_but_clicked(self,widget):
        settings = settings_win.MainWindow()
        print(win)
        settings.connect("delete-event", settings.destroy)
        settings.show_all()
        pass

    def change_dir(self, widget):
        yt_install.directory = self.dir_entry.get_text()
        #print(yt_install.directory)

    #settingsden bu bölüm eklenebilir olmaıl mı ?
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
            installation_type = self.protocol_combo.get_active_text()
            install_thread = threading.Thread(target = yt_install.download, args = [self.entered_url,installation_type])
            print("installation done")
            install_thread.start()

    def loop_stoped(self):
        #tüm install list_store yi boşaltır
        self.iSongStore.clear()
        self.progressbar.set_fraction(0)
        self.spinner.stop()

    def install_list(self,widget):
        install_list = [] # url list
        installation_type = self.protocol_combo.get_active_text()
        for row in self.iSongStore:
            install_list.append(row[2])
        #iSongStore
        if len(install_list) != 0:
            install_thread = threading.Thread(target = yt_install.loop, args = [install_list,self,installation_type])
            install_thread.start()

    def on_button_clicked(self, widget):
        link_list = yt_install.set_link_list()
        installation_type = self.protocol_combo.get_active_text()
        line = yt_install.loop(link_list,installation_type)
        #label olarak eklenebilir.
        #print("installation compleated.",line," sound downloaded")

def quit_app(arg):
    print("quiting..")
    Gtk.main_quit()
    print("All Done")

#if not t1.isAlive(): is thread alive
"""

win = MyWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
