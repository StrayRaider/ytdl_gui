from gi.repository import GObject, Gtk

class SongWidget():
    def __init__(self,name):
        self.id = name
        print(self.id)
        self.obj_l = []
        label = Gtk.Label()
        self.obj_l.append(label)

        checkbutton = Gtk.CheckButton(label="CheckButton")
        checkbutton.connect("toggled", self.on_check_button_toggled)
        self.obj_l.append(checkbutton)

    def on_check_button_toggled(self, checkbutton):
        if checkbutton.get_active():
            print("CheckButton toggled on!")
        else:
            print("CheckButton toggled off!")
