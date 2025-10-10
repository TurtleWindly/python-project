from kivy.uix.screenmanager import ScreenManager, Screen

from kivy.app import App

from app.views.homescreen.homescreen import HomeScreen
from app.views.quizscreen.quizscreen import QuizScreen
from app.views.registerscreen.registerscreen import RegisterScreen
from app.views.pdfscreen.pdfscreen import PdfScreen
from app.views.settingscreen.settingscreen import SettingScreen
from app.views.videoscreen.videoscreen import VideoScreen

# Create the manager


class MainApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomeScreen())
        sm.add_widget(SettingScreen())
        sm.add_widget(RegisterScreen())
        sm.add_widget(QuizScreen())
        sm.add_widget(PdfScreen())
        sm.add_widget(VideoScreen())
        return sm

    def on_start(self):
        self.root.current = "home_screen"


if __name__ == "__main__":
    MainApp().run()
