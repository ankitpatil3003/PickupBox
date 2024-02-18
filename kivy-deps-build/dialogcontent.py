# dialogcontent.py
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.menu import MDDropdownMenu
from kivy.properties import StringProperty


class DialogContent(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.spacing = "12dp"
        self.size_hint_y = None
        self.height = "400dp"
        self.cat = ""

        # self.name_input = MDTextField(hint_text="Product Name")
        # self.add_widget(self.name_input)

    def open_category_menu(self):
        self.menu_list = [
            {
                "viewclass": "OneLineListItem",
                "text": "electronics",
                "on_release": lambda x="electronics": self.electronics()
            },
            {
                "viewclass": "OneLineListItem",
                "text": "decor",
                "on_release": lambda x="decor": self.decor()
            }
        ]
        self.menu = MDDropdownMenu(
            caller=self.ids.menu_,
            items=self.menu_list,
            width_mult=4
        )
        self.menu.open()

    def electronics(self):  
        self.cat = "electronics"

    def decor(self):
        self.cat = "decor"
   

    
    

    # def test3(self):
    #     print("test3")
    