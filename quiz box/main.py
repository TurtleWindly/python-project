from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp

from app.views.homescreen.homescreen import HomeScreen
from app.views.registerscreen.registerscreen import RegisterScreen
from app.views.quizscreen.quizscreen import QuizScreen
from app.views.resultscreen.resultscreen import ResultScreen
from app.views.pdfscreen.pdfscreen import PdfScreen
from app.views.settingscreen.settingscreen import SettingScreen
from app.views.videoscreen.videoscreen import VideoScreen
from app.database import QuizDatabase

from app.user import User
from app.setting import AppSettings


# Create the manage
class MainApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = QuizDatabase()
        self.settings = AppSettings()
        self.current_user = User("", "")
        self.root = MDScreenManager()

    def on_start(self):
        self.root.current = "home_screen"

    def on_stop(self):
        self.db.close()


if __name__ == "__main__":
    MainApp().run()
