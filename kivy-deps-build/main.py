from productsmapview import ProductsMapView, ProductMarker
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from dialogcontent import DialogContent
import csv

class MainApp(MDApp):
    dialog = None

    def build(self):
        self.theme_cls.primary_palette = "Blue"
        map_view = ProductsMapView()
        map_view.add_product_markers('/Users/abhishekmhatre/Documents/BUhack/products.csv')  # Ensure this path is correct
        return map_view  # Return a single instance

    def show_add_product_dialog(self, lat, lon):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Add New Product:",
                type="custom",
                content_cls=DialogContent(),
                buttons=[
                    MDFlatButton(text="CANCEL", on_release=lambda x: self.dialog.dismiss()),
                    MDFlatButton(text="ADD", on_release=lambda x: self.add_product(lat, lon))
                ],
            )
        self.dialog.open()

    def add_product(self, lat, lon):
        product_name = self.dialog.content_cls.ids.name_input.text
        product_category = self.dialog.content_cls.cat
        self.save_to_csv(product_name, product_category, lat, lon)
        self.dialog.dismiss()

    def save_to_csv(self, name, category, lat, lon):
        with open('/Users/abhishekmhatre/Documents/BUhack/products.csv', 'a', newline='', encoding='utf-8') as file:  # Ensure this path is correct
            writer = csv.writer(file)
            writer.writerow([name, category, lat, lon])

    def show_product_info_dialog(self, name, category):
        dialog = MDDialog(title=name, text=f'Category: {category}')
        dialog.open()

if __name__ == "__main__":
    MainApp().run()
