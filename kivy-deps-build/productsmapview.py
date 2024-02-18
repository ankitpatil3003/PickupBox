from kivy_garden.mapview import MapMarker, MapView
from kivy.clock import Clock
from kivy.app import App
import time  # Ensure time is imported
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from dialogcontent import DialogContent
import csv

class ProductMarker(MapMarker):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size = (50, 50)
    product_name = ""
    product_category = ""

    def on_release(self):
        app = App.get_running_app()
        app.show_product_info_dialog(self.product_name, self.product_category)


class DraggableMarker(MapMarker):
    def __init__(self, **kwargs):
        super(DraggableMarker, self).__init__(**kwargs)
        self.is_being_dragged = False
        self.click_timeout = None
        self.double_click_delay = 0.25  # Seconds to wait for a second click

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if self.click_timeout:
                # A second click occurred, we can consider this a double-click
                self.click_timeout.cancel()  # Cancel the scheduled callback
                self.click_timeout = None
                self.open_dialog()
            else:
                self.is_being_dragged = True
                # This is the first click, we schedule a callback to reset the timeout
                self.click_timeout = Clock.schedule_once(self.reset_click_timeout, self.double_click_delay)
            return True
        return super(DraggableMarker, self).on_touch_down(touch)

    def reset_click_timeout(self, dt):
        # Reset the timeout, this method is called if a second click doesn't occur
        self.click_timeout = None

    def open_dialog(self):
        # Open the dialog content
        app = App.get_running_app()
        app.show_add_product_dialog(lat=self.lat, lon=self.lon)

    def on_touch_move(self, touch):
        if self.is_being_dragged:
            # Ensure that we are calling get_latlon_at on the MapView instance
            map_view = self.get_mapview()
            if map_view:
                lat, lon = map_view.get_latlon_at(touch.x, touch.y)
                self.lat = lat
                self.lon = lon
                return True
        return super(DraggableMarker, self).on_touch_move(touch)

    def on_touch_up(self, touch):
        if self.is_being_dragged:
            self.is_being_dragged = False
            return True
        return super(DraggableMarker, self).on_touch_up(touch)

    def get_mapview(self):
        # Navigate up the parent hierarchy to find the MapView instance
        parent = self.parent
        while parent is not None:
            if isinstance(parent, MapView):
                return parent
            parent = parent.parent
        return None
class ProductsMapView(MapView):
    def on_parent(self, instance, value):
        # Correctly initialize and add a marker when the view is added to its parent
        lat, lon = 42.0987, -75.918  # Example coordinates
        self.add_draggable_marker(lat, lon)

    def add_draggable_marker(self, lat, lon):
        marker = DraggableMarker(lat=lat, lon=lon, source="/Users/abhishekmhatre/Documents/BUhack/kivy-deps-build/marker.png")
        self.add_widget(marker)

    # Implement additional methods as needed
    getting_products_timer = None

    def start_getting_products_in_fov(self):
        try:
            self.getting_products_timer.cancel()
        except:
            pass
        self.getting_products_timer = Clock.schedule_once(self.get_markets_in_fov, 1)

    def get_markets_in_fov(self, *args):
        pass  
    
    def on_release(self):
        # Display the product information when the marker is clicked
        app = App.get_running_app()
        app.show_product_info_dialog(self.product_name, self.product_category)

    def add_product_markers(self, csv_path='/Users/abhishekmhatre/Documents/BUhack/products.csv'):
        try:
            with open(csv_path, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    try:
                        lat = float(row['lat'])
                        lon = float(row['lon'])
                        marker = ProductMarker(lat=lat, lon=lon, source='kivy-deps-build/box.png')
                        marker.product_name = row['name']
                        marker.product_category = row['category']
                        self.add_widget(marker)
                    except KeyError as e:
                        print(f"Missing key in CSV: {e}")
                    except ValueError:
                        print("Invalid lat/lon value")
        except FileNotFoundError:
            print("CSV file not found")