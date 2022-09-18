import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from yt_lib import yt_install

import threading

class MyWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Youtube Installation")
        #ana alanın oluşturulması
        self.main_box = Gtk.HBox()
        self.add(self.main_box)

        #ekran şeması çıkartılması
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
        
        #  arama bölümünün oluşturulması
        new_box = Gtk.HBox()
        m_cnt_box.pack_start(new_box,0,0,10)

        #arama entry
        self.search_entry = Gtk.Entry()
        self.search_entry.set_placeholder_text("Type")
        new_box.pack_start(self.search_entry,0,0,10)
        #arama but
        but_box = Gtk.HBox()
        m_cnt_box.pack_start(but_box,0,0,10)
        new_box = Gtk.HBox()
        but_box.pack_start(new_box,0,0,0)
        self.button = Gtk.Button(label=" Search ")
        self.button.connect("clicked", self.search) 
        new_box.pack_start(self.button,0,0,10)

        adjustment = Gtk.Adjustment(value=0,
                                    lower=0,
                                    upper=10,
                                    step_increment=1,
                                    page_increment=5,
                                    page_size=0)
        self.song_count_b = Gtk.SpinButton(adjustment=adjustment)
        new_box.pack_start(self.song_count_b,0,0,0)


        #settings bölümü
        top_box = Gtk.HBox()
        m_down_box.pack_start(top_box,0,0,10)
        self.settings_button = Gtk.Button(label = "Settings")
        self.settings_button.connect("clicked", self.settings_but_clicked)
        m_down_box.pack_start(self.settings_button,0,0,10)

        #indirme bölümü
        install_box = Gtk.VBox()
        m_up_box.pack_start(install_box,0,0,0)

        #indirme entry
        new_box = Gtk.HBox()
        install_box.pack_start(new_box,0,0,10)
        self.url_entry = Gtk.Entry()
        self.url_entry.set_placeholder_text("Paste Url Here")
        new_box.pack_start(self.url_entry,0,0,10)

        #directory entry
        new_box = Gtk.HBox()
        install_box.pack_start(new_box,0,0,10)
        self.dir_entry = Gtk.Entry()
        self.dir_entry.set_placeholder_text("directory")
        new_box.pack_start(self.dir_entry,0,0,10)
        but_box = Gtk.HBox()
        install_box.pack_start(but_box,0,0,10)

        #install but
        new_box = Gtk.HBox()
        but_box.pack_start(new_box,0,0,0)
        self.button = Gtk.Button(label=" Install ")
        self.button.connect("clicked", self.install_one_song) 
        new_box.pack_start(self.button,0,0,10)

        #----------------------------------İndirilecekler Listesi
        #treeview ve list store oluşturulması
        #list store oluştururken sütunların hangi tipte değişken tutacağı belirtilir
        self.iSongStore = Gtk.ListStore(str,bool)
        self.iSongTree = Gtk.TreeView(self.iSongStore)
        #içinde tutacağı değişken tipine göre bölme oluşturulması
        cell = Gtk.CellRendererText()
        #cell.set_property("editable", True) #eğer tect değiştirilebilir olsun istersen
        #stun tanımlama işlemi 1. argüman stun adı, 2. tutacağı hücre tipi 3, ekleme
        #yaparken listenin kaçıncı argümanını alacağı
        column = Gtk.TreeViewColumn("deneme",cell,text = 0)

        #check button stunu oluşturma işlemi
        #uygun hücre oluşturma
        check_cell = Gtk.CellRendererToggle()
        #hücre içi widget fonksiyon bağlantısı
        check_cell.connect("toggled", self.tree_but_toggle,1)
        #satır oluşturma 1. satır adı 2. hücre tipi
        t_column = Gtk.TreeViewColumn("deneme",check_cell)
        #stuna argümanları dışarda bu fonksiyonla da verebilirsin
        t_column.add_attribute(check_cell,"active",1)

        #stun treeview ekleme işlemi
        self.iSongTree.append_column(t_column)
        self.iSongTree.append_column(column)
 
        #yeni satırlar oluşturma
        self.iSongStore.append(["deneme",True])
        self.iSongStore.append(["deneme",False])
        left_box.set_size_request(300,500)
        l_scrolled = Gtk.ScrolledWindow()
        left_box.pack_start(l_scrolled,1,1,10)
        l_scrolled.add(self.iSongTree)


        #--------------------------------Arama Sonucu Listesi
        #treeview ve list store oluşturulması
        #list store oluştururken sütunların hangi tipte değişken tutacağı belirtilir
        self.sSongStore = Gtk.ListStore(str,bool)
        self.sSongTree = Gtk.TreeView(self.sSongStore)
        #içinde tutacağı değişken tipine göre bölme oluşturulması
        cell = Gtk.CellRendererText()
        #cell.set_property("editable", True) #eğer tect değiştirilebilir olsun istersen
        #stun tanımlama işlemi 1. argüman stun adı, 2. tutacağı hücre tipi 3, ekleme
        #yaparken listenin kaçıncı argümanını alacağı

        search_s_n = "searched song name"
        search_t_n = "wanna install ?"
        column = Gtk.TreeViewColumn(search_s_n,cell,text = 0)

        #check button stunu oluşturma işlemi
        #uygun hücre oluşturma
        check_cell = Gtk.CellRendererToggle()
        #hücre içi widget fonksiyon bağlantısı
        check_cell.connect("toggled", self.tree_but_toggle,1)
        #satır oluşturma 1. satır adı 2. hücre tipi
        t_column = Gtk.TreeViewColumn(search_t_n,check_cell)
        #stuna argümanları dışarda bu fonksiyonla da verebilirsin
        t_column.add_attribute(check_cell,"active",1)

        #stun treeview ekleme işlemi
        self.sSongTree.append_column(t_column)
        self.sSongTree.append_column(column)
 
        #yeni satırlar oluşturma
        self.sSongStore.append(["song_title",True])
        self.sSongStore.append(["song_title",False])
        right_box.set_size_request(300,500)
        r_scrolled = Gtk.ScrolledWindow()
        right_box.pack_start(r_scrolled,1,1,10)
        r_scrolled.add(self.sSongTree)


    def addToStore(self, obj_list, store, is_tick):
        for obj in obj_list:
            store.append([obj[0],is_tick])

    def tree_but_toggle(self, widget, path, column):
        print(path,column)
        self.sSongStore[path][column] = not self.sSongStore[path][column]
        print("toggled")

    def add_into_install(self,widget):
        pass

    def search(self, widget):
        search_count = self.song_count_b.get_value_as_int()
        entry = self.search_entry.get_text()
        search_thread = threading.Thread(target =yt_install.search, args = [entry])
        search_thread.start()
        yt_install.search(entry,search_count)
        self.s_song_list = yt_install.song_list
        print(self.s_song_list)
        self.addToStore(self.s_song_list,self.sSongStore, False)

    def paste_into_install(self,widget):
        pass

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
