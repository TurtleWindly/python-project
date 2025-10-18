from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty


class SettingScreen(Screen):
    name = "setting_screen"

    max_question_text = ObjectProperty(None)
    volume_text = ObjectProperty(None)

    def __init__(self, **kw):
        super().__init__(**kw)
        app = App.get_running_app()
        self.max_question_text = app.settings.max_question
        self.volume_text = app.settings.volume

    def save(self):
        app = App.get_running_app()
        app.settings.max_question = self.max_question_text
        app.settings.volume = self.volume_text
        app.settings.save()
