from kivy.lang import Builder
from kivymd.uix.label import MDLabel
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivy.config import Config
import time; 
import requests; 
import json; 
from kivy.uix.label import Label
from kivy.core.window import Window
from amadeus import Client, Location, ResponseError
import requests


amadeus = Client(
    client_id='awcKZ2oK2A6umtnIhzKHE1SGC9LcDNkF',
    client_secret='gFBeJtNGyTWAuxkI'
)

response = amadeus.travel.predictions.flight_delay.get(originLocationCode='ORD',
destinationLocationCode='LHR', departureDate='2024-10-19', carrierCode='BA', flightNumber='296')

print(response.data)

KV = '''
ScreenManager:
    MainScreen:

<MainScreen>:
    name: 'main'
    MDTextField:
        id: text_field
        hint_text: "Where do you want to go?"
        pos_hint: {"center_x": 0.51, "center_y": 0.7}
        size_hint_x: None
        width: 300
    MDTextField:
        id: text_field
        hint_text: "What is your flight number?"
        pos_hint: {"center_x": 0.51, "center_y": 0.6}
        size_hint_x: None
        width: 300
    MDRaisedButton:
        text: "Submit"
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        on_release: app.on_button_press()
'''
class Header(MDLabel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = "OnePass"
        self.halign = "center"
        self.pos_hint = {"center_x": 0.5, "center_y": 0.9}
        self.font_style = "H6"


class MainScreen(Screen):
    pass

class MainApp(MDApp):
    def build(self):
        self.start_time = time.time()
        Window.size = (400, 600)
        return Builder.load_string(KV)

    def on_button_press(self):
        text = self.root.get_screen('main').ids.text_field.text
        print(f'Text entered: {text}')

    def on_stop(self):
        end_time = time.time()
        print(f'Time taken: {(int) (end_time - self.start_time)}')
        

if __name__ == '__main__':
    MainApp().run()