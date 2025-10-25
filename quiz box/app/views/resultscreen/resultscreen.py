from kivy.app import App
from kivymd.uix.screen import MDScreen
from kivy.properties import ObjectProperty

from app.user import User

class ResultScreen(MDScreen):
    name = "result_screen"
    name_label = ObjectProperty(None)
    unit_label = ObjectProperty(None)
    score_label = ObjectProperty(None)

    def on_enter(self, **kw):
        app = App.get_running_app()

        self.name_label.text = app.current_user.name
        self.unit_label.text = app.current_user.unit
        self.score_label.text = str(app.current_user.score)

        # Clear the score after displaying it
        app.current_user.score = 0

