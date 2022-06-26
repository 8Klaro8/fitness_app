from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.button import ButtonBehavior
from kivy.uix.image import Image
from workout_banner import WorkoutBanner
from kivy.uix.label import Label
import requests
import json
import os
from os import walk
from functools import partial
from myfirebase import MyFireBase
from firebase_admin import db
# import os
# from dotenv import load_dotenv
# load_dotenv()

# Learning source: https://www.youtube.com/watch?v=rnzRnzEZu40&list=PLy5hjmUzdc0lo7EJM0UDMMN35nWqb3_Ei&index=5

PRIVATE_KEY_PATH = os.getenv('PRIVATE_KEY_PATH')


class HomeScreen(Screen):
    pass
class LabelButton(ButtonBehavior, Label):
    pass
class ImageButton(ButtonBehavior, Image):
    pass
class ChangeAvatarScreen(Screen):
    pass
class LoginScreen(Screen):
    pass

class SettingsScreen(Screen):
    pass


GUI = Builder.load_file('main.kv')
class MainApp(App):
    my_friend_id = 1
    def build(self):
        self.my_firebase = MyFireBase()
        return GUI

    def on_start(self):

        # ref = db.reference(
        #     'https://friendly-fitness-9b323-default-rtdb.firebaseio.com/'
        # )
        # print(ref.get())
        # quit()

        # Populate avatar grid
        avatar_grid = self.root.ids['change_avatar_screen'].ids['avatar_grid']
        for root_dir, folder, file in walk("avatars"):
            for f in file:
                img = ImageButton(source="avatars/" + f, on_release=partial(self.change_avatar, f))
                avatar_grid.add_widget(img)

        # Try to read the persisten signin credentials (refresh token)
        try:
            with open("refresh_token.txt", 'r') as f:
                refresh_token = f.read()

            # Use refresh token to get a new idToken
            id_token, local_id = self.my_firebase.exchange_refresh_token(refresh_token)


            # Get database data
            result = requests.get(
                'https://friendly-fitness-9b323-default-rtdb.firebaseio.com/' + local_id + '.json?auth=' + id_token)
            data = result.json()
            print(f'data: {data}')
            print("WAS OK?" + f'{result.ok}')

            # Get and update avatar image
            avatar_image = self.root.ids['avatar_image']
            avatar_image.source = "avatars/" + data['avatar']
            print(f'avatar image source: {avatar_image.source}')
            workouts = data['workouts'][1:]
            print('here')
            # quit()

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

            self.change_screen('home_screen')

        except Exception as e:
            print(f'Something wrong with: {e}')
            pass


    def change_screen(self, screen_name):

        # Gets the screen manager from the root
        screen_manager = self.root.ids['screen_manager']

        # Sets the current screen to the screen that was passed
        # in as parameter in homescreen.kv - app.change_screen
        screen_manager.current = screen_name

    def change_avatar(self, image, widget_id):
        # Change avatar in the app
        current_avatar_image = self.root.ids['avatar_image']
        current_avatar_image.source = "avatars/" + image

        # Change avatar in Firebase
        my_data = '{"avatar": "%s"}' % image
        requests.patch(
            'https://friendly-fitness-9b323-default-rtdb.firebaseio.com/' + f'{str(self.my_friend_id)}' + '.json', data=my_data)
        self.change_screen("settings_screen")


MainApp().run()

