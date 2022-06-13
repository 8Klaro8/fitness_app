from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.button import ButtonBehavior
from kivy.uix.image import Image
import requests
import json

# Learning source: https://www.youtube.com/watch?v=rnzRnzEZu40&list=PLy5hjmUzdc0lo7EJM0UDMMN35nWqb3_Ei&index=5


class HomeScreen(Screen):
    pass
class ImageButton(ButtonBehavior, Image):
    pass

class SettingsScreen(Screen):
    pass


GUI = Builder.load_file('main.kv')
class MainApp(App):
    my_friend_id = 1
    def build(self):
        return GUI

    def on_start(self):
        # Get database data
        result = requests.get(
            'https://friendly-fitness-9b323-default-rtdb.firebaseio.com/' + f'{str(self.my_friend_id)}' + '.json')
        data = result.json()
        print(data)
        # Get and update avatar image
        avatar_image = self.root.ids['home_screen'].ids['avatar_image']
        avatar_image.source = "icons/" + data['avatar']
        workouts = data['workouts'][1:]
        # Get and update streak label
        streak_label = self.root.ids['home_screen'].ids['streak_label']
        streak_label.text = str(data['streak']) + ' Day Streak!'
        for workout in workouts:
            # Populate workout grid on home screen
            print(workout['workout_image'])
            print(workout['units'])

    def change_screen(self, screen_name):

        # Gets the screen manager from the root
        screen_manager = self.root.ids['screen_manager']

        # Sets the current screen to the screen that was passed
        # in as parameter in homescreen.kv - app.change_screen
        screen_manager.current = screen_name

MainApp().run()

