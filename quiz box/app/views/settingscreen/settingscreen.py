from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.properties import ObjectProperty, NumericProperty


class SettingScreen(MDScreen):
    name = "setting_screen"

    max_question_text = ObjectProperty(None)
    volume = NumericProperty(None)

    def __init__(self, **kw):
        super().__init__(**kw)
        app = MDApp.get_running_app()
        self.max_question_text = app.settings.max_question
        self.volume = app.settings.volume

    def save(self):
        app = MDApp.get_running_app()
        app.settings.max_question = self.max_question_text
        app.settings.volume = self.volume
        app.settings.save()
