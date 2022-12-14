import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from yt_lib import yt_install, settings_win

import threading

class MyWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Youtube Installation")

        # adding main box
        self.main_box = Gtk.HBox()
        self.add(self.main_box)

        #screen tiles etc..
        left_box = Gtk.Box()
        right_box = Gtk.Box()
        mid_box = Gtk.VBox()
        m_up_box = Gtk.VBox()
        m_cnt_box = Gtk.VBox()
        m_down_box = Gtk.VBox()
        self.main_box.pack_start(left_box,1,1,10)
        self.main_box.pack_start(mid_box,1,1,10)
        self.main_box.pack_start(right_box,1,1,10)
        mid_box.pack_start(m_up_box,0,0,0)
        mid_box.pack_start(m_cnt_box,0,0,0)
        mid_box.pack_start(m_down_box,0,0,0)
        x = 400
        y = 700
        right_box.set_size_request(x, y)
        left_box.set_size_request(x, y)


        #Search Part
        new_box = Gtk.HBox()
        m_cnt_box.pack_start(new_box,0,0,10)

        #Search entry
        self.search_entry = Gtk.Entry()
        self.search_entry.set_placeholder_text("Type")
        new_box.pack_start(self.search_entry,0,0,10)

        #Search button
        but_box = Gtk.HBox()
        m_cnt_box.pack_start(but_box,0,0,10)
        new_box = Gtk.HBox()
        but_box.pack_start(new_box,0,0,0)
        self.button = Gtk.Button(label=" Search ")
        self.button.connect("clicked", self.search) 
        new_box.pack_start(self.button,0,0,10)

        # adjustments for spin_button
        adjustment = Gtk.Adjustment(value=0,
                                    lower=1,
                                    upper=20,
                                    step_increment=1,
                                    page_increment=5,
                                    page_size=0)
        self.song_count_b = Gtk.SpinButton(adjustment=adjustment)
        new_box.pack_start(self.song_count_b,0,0,0)


        #settings Part
        top_box = Gtk.HBox()
        m_down_box.pack_start(top_box,0,0,10)
        self.settings_button = Gtk.Button(label = "Settings")
        self.settings_button.connect("clicked", self.settings_but_clicked)
        m_down_box.pack_start(self.settings_button,0,0,10)

        #installation Part
        install_box = Gtk.VBox()
        m_up_box.pack_start(install_box,0,0,0)

        #install entry
        new_box = Gtk.HBox()
        install_box.pack_start(new_box,0,0,10)
        self.url_entry = Gtk.Entry()
        self.url_entry.set_placeholder_text("Song's Url")
        new_box.pack_start(self.url_entry,0,0,10)

        self.title_entry = Gtk.Entry()
        self.title_entry.set_placeholder_text("Song's Title")
        new_box.pack_start(self.title_entry,0,0,10)


        nVBox = Gtk.VBox()
        install_box.pack_start(nVBox,0,0,0)
        self.add_button = Gtk.Button(label=" Add ")
        #self.button.connect("clicked", self.install_one_song) 
        self.add_button.connect("clicked", self.add_song)
        nVBox.pack_start(self.add_button,0,0,0)

        #directory entry
        new_box = Gtk.HBox()
        install_box.pack_start(new_box,0,0,10)
        self.dir_entry = Gtk.Entry()
        self.dir_entry.set_placeholder_text("directory")
        new_box.pack_start(self.dir_entry,0,0,10)

        #set dir but
        #new_box = Gtk.HBox()
        install_box.pack_start(new_box,1,1,0)
        self.add_button = Gtk.Button(label="Set Directory")
        #self.button.connect("clicked", self.install_one_song) 
        self.add_button.connect("clicked", self.change_dir)
        new_box.pack_start(self.add_button,0,0,0)

        #install but
        nVBox = Gtk.VBox()
        install_box.pack_start(nVBox,0,0,10)
        self.button = Gtk.Button(label=" Install ")
        #self.button.connect("clicked", self.install_one_song) 
        self.button.connect("clicked", self.install_list)
        nVBox.pack_start(self.button,0,0,10)

        #spinner
        self.spinner = Gtk.Spinner()
        new_box.pack_start(self.spinner,0,0,0)

        #----------------------------------??ndirilecekler Listesi
        #treeview ve list store olu??turulmas??
        #list store olu??tururken s??tunlar??n hangi tipte de??i??ken tutaca???? belirtilir
        self.iSongStore = Gtk.ListStore(str,bool,str,bool)
        self.iSongTree = Gtk.TreeView(self.iSongStore)
        #i??inde tutaca???? de??i??ken tipine g??re b??lme olu??turulmas??
        cell = Gtk.CellRendererText()
        cell.set_property("editable", True) #e??er tect de??i??tirilebilir olsun istersen
        #stun tan??mlama i??lemi 1. arg??man stun ad??, 2. tutaca???? h??cre tipi 3, ekleme
        #yaparken listenin ka????nc?? arg??man??n?? alaca????
        column = Gtk.TreeViewColumn("Song To Download",cell,text = 0)
        column.set_max_width(200)
        u_column = Gtk.TreeViewColumn("Url",cell,text = 2)

        #check button stunu olu??turma i??lemi
        #uygun h??cre olu??turma
        check_cell = Gtk.CellRendererToggle()
        del_cell = Gtk.CellRendererToggle()
        #h??cre i??i widget fonksiyon ba??lant??s??
        check_cell.connect("toggled", self.tree_but_toggle,1,"i")
        del_cell.connect("toggled", self.del_tree_obj,3,"i")
        #sat??r olu??turma 1. sat??r ad?? 2. h??cre tipi
        t_column = Gtk.TreeViewColumn("->",check_cell)
        del_column = Gtk.TreeViewColumn("del",del_cell)
        #stuna arg??manlar?? d????arda bu fonksiyonla da verebilirsin
        t_column.add_attribute(check_cell,"active",1)
        u_column.set_max_width(70)
        t_column.set_max_width(30)
        del_column.set_max_width(30)

        #stun treeview ekleme i??lemi
        self.iSongTree.append_column(t_column)
        self.iSongTree.append_column(del_column)
        self.iSongTree.append_column(u_column)
        self.iSongTree.append_column(column)
 
        #yeni sat??rlar olu??turma
        #self.iSongStore.append(["song_name",True,"url"])
        l_scrolled = Gtk.ScrolledWindow()
        left_box.pack_start(l_scrolled,1,1,10)
        l_scrolled.add(self.iSongTree)

        #--------------------------------Arama Sonucu Listesi
        #treeview ve list store olu??turulmas??
        #list store olu??tururken s??tunlar??n hangi tipte de??i??ken tutaca???? belirtilir
        self.sSongStore = Gtk.ListStore(str,bool,str,bool)
        self.sSongTree = Gtk.TreeView(self.sSongStore)
        #i??inde tutaca???? de??i??ken tipine g??re b??lme olu??turulmas??
        cell = Gtk.CellRendererText()
        cell.set_property("editable", True) #e??er tect de??i??tirilebilir olsun istersen
        #cell.set_property("editable", True) #e??er tect de??i??tirilebilir olsun istersen
        #stun tan??mlama i??lemi 1. arg??man stun ad??, 2. tutaca???? h??cre tipi 3, ekleme
        #yaparken listenin ka????nc?? arg??man??n?? alaca????

        column = Gtk.TreeViewColumn("searched song name",cell,text = 0)
        u_column = Gtk.TreeViewColumn("Url",cell,text = 2)
        #check button stunu olu??turma i??lemi
        #uygun h??cre olu??turma
        check_cell = Gtk.CellRendererToggle()
        del_cell = Gtk.CellRendererToggle()
        #h??cre i??i widget fonksiyon ba??lant??s??
        check_cell.connect("toggled", self.tree_but_toggle, 1, "s")
        del_cell.connect("toggled", self.del_tree_obj, 3, "s")
        #sat??r olu??turma 1. sat??r ad?? 2. h??cre tipi
        t_column = Gtk.TreeViewColumn("<-",check_cell)
        del_column = Gtk.TreeViewColumn("del",del_cell)
        #stuna arg??manlar?? d????arda bu fonksiyonla da verebilirsin
        t_column.add_attribute(check_cell,"active",1)
        u_column.set_max_width(70)
        t_column.set_max_width(30)
        del_column.set_max_width(30)
        self.sSongTree.append_column(t_column)
        self.sSongTree.append_column(del_column)
        self.sSongTree.append_column(u_column)
        self.sSongTree.append_column(column)
 
        #yeni sat??rlar olu??turma
        #self.sSongStore.append(["song_title",False,"Url"])
        #self.sSongStore.append(["song_title",False,"Url"])
        r_scrolled = Gtk.ScrolledWindow()
        right_box.pack_start(r_scrolled,1,1,10)
        r_scrolled.add(self.sSongTree)
        #print(self.iSongStore.get_iter())

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
        #bas??lmadan ??nceki hali
        #print(self.sSongStore[path][column])#true ya da false d??ner
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

    #settingsden bu b??l??m eklenebilir olma??l m?? ?
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

    def loop_stoped(self):
        #t??m install list_store yi bo??alt??r
        self.iSongStore.clear()
        self.spinner.stop()

    def install_list(self,widget):
        install_list = [] # url list
        for row in self.iSongStore:
            install_list.append(row[2])
        #iSongStore
        if len(install_list) != 0:
            install_thread = threading.Thread(target = yt_install.loop, args = [install_list,self])
            install_thread.start()

    def on_button_clicked(self, widget):
        link_list = yt_install.set_link_list()
        line = yt_install.loop(link_list)
        #label olarak eklenebilir.
        #print("installation compleated.",line," sound downloaded")

def quit_app(arg):
    print("quiting..")
    Gtk.main_quit()
    print("All Done")

#if not t1.isAlive(): is thread alive

win = MyWindow()
win.connect("destroy", quit_app)
win.show_all()
Gtk.main()
