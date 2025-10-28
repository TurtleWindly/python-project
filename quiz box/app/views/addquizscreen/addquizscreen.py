from kivy.app import App
from kivymd.uix.screen import MDScreen
from kivy.properties import ObjectProperty

# from app.user import User

class AddQuizScreen(MDScreen):
    name = "add_quiz_screen"

    # def on_enter(self, **kw):
    #     app = App.get_running_app()

    #     self.score_label.text += str(app.current_user.score) + "/" + str(app.settings.max_question)

    #     # Clear the score after displaying it
    #     app.current_user.score = 0

