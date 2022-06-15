from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.button import ButtonBehavior
from kivy.uix.image import Image
from workout_banner import WorkoutBanner
from kivy.uix.label import Label
import requests
import json

# Learning source: https://www.youtube.com/watch?v=rnzRnzEZu40&list=PLy5hjmUzdc0lo7EJM0UDMMN35nWqb3_Ei&index=5


class HomeScreen(Screen):
    pass
class LabelButton(ButtonBehavior, Label):
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
        avatar_image = self.root.ids['avatar_image']
        avatar_image.source = "icons/" + data['avatar']
        workouts = data['workouts'][1:]

        # Get and update streak label
        streak_label = self.root.ids['home_screen'].ids['streak_label']
        streak_label.text = str(data['streak']) + ' Day Streak!'

        # Get and update friend ID label
        friend_id_label = self.root.ids['settings_screen'].ids['friend_id_label']
        friend_id_label.text = 'Friend ID: ' + str(data['friend_id_label'])


        # Get banner grid
        banner_grid = self.root.ids['home_screen'].ids['banner_grid']

        for workout in workouts:
            for i in range(5):
                # Populate workout grid in home screen
                w = WorkoutBanner(workout_image=workout['workout_image'], description=workout['description'],
                                  type_image=workout['type_image'], number=workout['number'], units=workout['units'],
                                  likes=workout['likes'])
                banner_grid.add_widget(w)

    def change_screen(self, screen_name):

        # Gets the screen manager from the root
        screen_manager = self.root.ids['screen_manager']

        # Sets the current screen to the screen that was passed
        # in as parameter in homescreen.kv - app.change_screen
        screen_manager.current = screen_name

MainApp().run()

