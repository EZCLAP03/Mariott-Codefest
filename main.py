from kivy.lang import Builder
from kivymd.uix.label import MDLabel
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.menu import MDDropdownMenu
from kivy.metrics import dp
from kivy.clock import Clock
import time 
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy_garden.mapview import MapView, MapMarker

KV = '''
ScreenManager:
    MainScreen:
    MapScreen:

<MainScreen>:
    name: 'main'
    FloatLayout:
        orientation: 'vertical'
        MDTextField:
            id: search_field
            hint_text: "Enter State Code"
            pos_hint: {"center_x": 0.51, "center_y": 0.6}
            size_hint_x: None
            icon_left: "layers-search-outline"
            width: 300
            on_text: app.give_suggestions()
        MDRaisedButton:
            text: "Submit"
            pos_hint: {"center_x": 0.5, "center_y": 0.5}
            on_release: app.on_button_press()
        MDRectangleFlatButton:
            text: "Hello, World"
            pos_hint: {"center_x": .5, "center_y": .2}
        MDRaisedButton:
            text: "Open Map"
            pos_hint: {"center_x": 0.5, "center_y": 0.4}
            on_release: app.create_map()

<MapScreen>:
    name: 'map'
    FloatLayout:
        orientation: 'vertical'
        FloatLayout:
            id: map_box
        MDRaisedButton:
            text: "Back"
            size_hint: None, None
            size: 100, 50
            pos_hint: {"center_x": 0.5, "center_y": 0.1}
            on_release: app.root.current = 'main'  
'''

class MainScreen(Screen):
    pass

class MapScreen(Screen):
    def on_enter(self):
        map_view = MapView(zoom=10, lat=37.7749, lon=-122.4194)  
        map_marker = MapMarker(lat=37.7749, lon=-122.4194)
        map_view.add_marker(map_marker)
        self.ids.map_box.add_widget(map_view)
        back_button = MDRaisedButton(
                text="Back",
                size_hint=(None, None),  # Use None to specify size manually
                size=(100, 50),  # Set an explicit size for the button
                pos_hint={"center_x": 0.5, "center_y": 0.1},  # Position at the bottom center
                on_release=lambda _: print("Back button pressed")  # Replace with your logic
            )
  

Window.size = (360, 640) 


class MainApp(MDApp):
    suggestions_source = [
    'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California',
    'Colorado', 'Connecticut', 'Delaware', 'Florida', 'Georgia',
    'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa',
    'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland',
    'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri',
    'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey',
    'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio',
    'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina',
    'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont',
    'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming'
]

    def build(self):
        self.theme_cls.theme_style = "Dark"  
        self.theme_cls.primary_palette = "Purple"
 
        self.menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": f"Item {i}",
                "height": dp(56),
                "on_release": lambda x=f"Item {i}": self.menu_callback(x),
            } for i in range(5)
        ]
        
        self.menu = MDDropdownMenu(
            caller=self.root,  # Set a valid caller
            items=self.menu_items,
            width_mult=4,
        )
        
        return Builder.load_string(KV)

    def on_button_press(self):
        state = self.root.get_screen('main').ids.search_field  # Correct ID reference
        print(f'Text entered: {state}')

    def create_map(self):
        self.root.current = 'map'
        map_box = self.root.get_screen('map').ids.map_box
        map_box.clear_widgets()

        # Create a simple map representation
        map_label = MDLabel(
            
            halign="center",
            theme_text_color="Primary"
        )
        map_box.add_widget(map_label)
    def go_back(self):
        self.root.current = 'main'

    def give_suggestions(self):
        if hasattr(self, 'dropdown'):
            self.dropdown.dismiss()
        self.dropdown = DropDown()
        box = self.root.get_screen('main').ids.search_field
        user_input = self.root.get_screen('main').ids.search_field
        suggestions = []

        user_input_text = user_input.text.lower()
        for word in self.suggestions_source:
            if user_input_text in word.lower():
                suggestions.append(word)

        # Add suggestions to the dropdown
        for suggestion in suggestions[:4]:  
            btn = Button(
                text=suggestion,
                size_hint_y=None,
                height='44dp',
                background_normal='',
                background_color=(0.2, 0.6, 0.8, 1),  
                color=(1, 1, 1, 1),
                font_size='16sp',
                border=(16, 16, 16, 16) 
            )
            btn.bind(on_release=lambda btn: select_suggestion(self, btn.text))
            
            self.dropdown.add_widget(btn)
            print(suggestion)
        self.dropdown.open(user_input)

        def select_suggestion(self, text):
            self.root.get_screen('main').ids.search_field.text = text
            self.dropdown.dismiss()



if __name__ == '__main__':
    MainApp().run()
