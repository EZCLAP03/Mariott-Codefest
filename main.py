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
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy_garden.mapview import MapView, MapMarker
import api

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
            hint_text: "Enter State"
            pos_hint: {"center_x": 0.51, "center_y": 0.7}
            size_hint_x: None
            icon_left: "layers-search-outline"
            width: 300
            on_text: app.give_suggestions()
        MDRectangleFlatButton:
            text: "Submit"
            pos_hint: {"center_x": 0.5, "center_y": 0.5}
            on_release: app.on_button_press()
        MDRectangleFlatButton:
            text: "Open Map"
            pos_hint: {"center_x": 0.5, "center_y": 0.4}
            on_release: app.create_map()
        MDTextField:
            id: search_field_2
            hint_text: "Enter County"
            pos_hint: {"center_x": 0.51, "center_y": 0.6}
            size_hint_x: None
            icon_left: "layers-search-outline"
            width: 300
            on_text: app.give_suggestions2()

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
        main_screen = self.manager.get_screen('main')
        state_text = main_screen.ids.search_field.text
        county_text = main_screen.ids.search_field_2.text

        lats = api.get_latitude(county_text, state_text)
        long = api.get_longtitude(county_text, state_text)
        lats = float(lats)
        long = float(long)
        map_view = MapView(zoom=10, lat=lats, lon=long)  
        map_marker = MapMarker(lat=lats, lon=long)
        map_view.add_marker(map_marker)
        self.ids.map_box.add_widget(map_view)
        back_button = MDRaisedButton(
                text="Back",
                size_hint=(None, None),  
                size=(100, 50),  
                pos_hint={"center_x": 0.5, "center_y": 0.1},  
                on_release=lambda _: print("Back button pressed")  
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
        self.theme_cls.primary_palette = "Gray"
 
        self.menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": f"Item {i}",
                "height": dp(56),
                "on_release": lambda x=f"Item {i}": self.menu_callback(x),
            } for i in range(5)
        ]
        
        self.menu = MDDropdownMenu(
            caller=self.root,  
            items=self.menu_items,
            width_mult=4,
        )
        
        return Builder.load_string(KV)

    def on_button_press(self):
        state = self.root.get_screen('main').ids.search_field
        state_text = state.text
        state1 = self.root.get_screen('main').ids.search_field_2
        state_text1 = state1.text
        
        if hasattr(self, 'state_label') and self.state_label:
            self.root.get_screen('main').remove_widget(self.state_label)
        if hasattr(self, 'state_label1') and self.state_label1:
            self.root.get_screen('main').remove_widget(self.state_label1)
        
        esg_score = api.get_score(state_text)
        if esg_score == "State not found":
            esg_score = "does not exist"
        else:
            esg_score = round(esg_score, 3)
        self.state_label = MDLabel(
            text=f"[color=#AAAAAA]ESG score: {esg_score}[/color]",
            markup=True,
            halign="center",
            theme_text_color="Primary",
            pos_hint={"center_x": 0.5, "center_y": 0.3},
            font_name="Roboto-Regular",
        )

        news = api.get_news(state_text1)
        self.state_label1 = MDLabel(
            text=f"[color=#AAAAAA]News: {news[0]}[/color]",
            markup=True,
            halign="center",
            theme_text_color="Primary",
            pos_hint={"center_x": 0.5, "center_y": 0.1},
            font_name="Roboto-Regular",
        )
        self.root.get_screen('main').add_widget(self.state_label)
        self.root.get_screen('main').add_widget(self.state_label1)

    def create_map(self):
        self.root.current = 'map'
        map_box = self.root.get_screen('map').ids.map_box
        map_box.clear_widgets()

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

        for suggestion in suggestions[:4]:  
            btn = Button(
                text=suggestion,
                size_hint_y=None,
                height='44dp',
                background_normal='',
                background_color=(0.5, 0.5, 0.5, 1),  
                color=(1, 1, 1, 1),
                font_size='16sp',
                border=(16, 16, 16, 16) 
            )
            btn.bind(on_release=lambda btn: select_suggestion(self, btn.text))
            
            self.dropdown.add_widget(btn)
        self.dropdown.open(user_input)

        def select_suggestion(self, text):
            self.root.get_screen('main').ids.search_field.text = text
            self.dropdown.dismiss()


    def give_suggestions2(self):
        if hasattr(self, 'dropdown'):
            self.dropdown.dismiss()
        self.dropdown = DropDown()
        box = self.root.get_screen('main').ids.search_field_2
        user_input = self.root.get_screen('main').ids.search_field_2
        suggestions = []

        user_input_text = user_input.text.lower()
        for word in api.get_county(self.root.get_screen('main').ids.search_field.text):
            if user_input_text in word.lower():
                suggestions.append(word)

        for suggestion in suggestions[:4]:  
            btn = Button(
                text=suggestion,
                size_hint_y=None,
                height='44dp',
                background_normal='',
                background_color=(0.5, 0.5, 0.5, 1),  
                color=(1, 1, 1, 1),
                font_size='16sp',
                border=(16, 16, 16, 16) 
            )
            btn.bind(on_release=lambda btn: select_suggestion(self, btn.text))
            
            self.dropdown.add_widget(btn)
        self.dropdown.open(user_input)

        def select_suggestion(self, text):
            self.root.get_screen('main').ids.search_field_2.text = text
            self.dropdown.dismiss()




if __name__ == '__main__':
    MainApp().run()
