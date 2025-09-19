from kivy.uix.screenmanager import ScreenManager, Screen

from kivy.app import App

from app.views.homescreen.homescreen import HomeScreen
from app.views.quizscreen.quizscreen import QuizScreen
from app.views.settingscreen.settingscreen import SettingScreen

# Create the manager


class MainApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomeScreen())
        sm.add_widget(SettingScreen())
        sm.add_widget(QuizScreen())
        return sm

    def on_start(self):
        self.root.current = "home_screen"


if __name__ == "__main__":
    MainApp().run()
