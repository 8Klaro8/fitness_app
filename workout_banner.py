from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label

class WorkoutBanner(GridLayout):
    # Got only one row
    rows = 1

    # Accepts kwargs - initialize it with positional values
    def __init__(self, **kwargs):
        # If there is kwargs that relate to the grid layout, then calls gridlayout
        super(WorkoutBanner, self).__init__()

        left = FloatLayout()
        left_image = Image(source='icons/' + kwargs['workout_image'], size_hint=(1, 0.8), pos_hint={"top": 1, "left": 1})
        left_label = Label(text=kwargs['description'], size_hint=(1, 0.2), pos_hint={"top": .2, "left": 1})
        left.add_widget(left_image)
        left.add_widget(left_label)

        self.add_widget(left)
