from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivy.properties import ObjectProperty

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
    screen_manager = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = QuizDatabase()
        self.settings = AppSettings()
        self.current_user = User("", "")
        self.screen_history = []  # lưu stack của các màn hình trước
        self._last_screen = None

    def build(self):
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.theme_style = "Light"

    def on_start(self):
        # lấy reference tới MDScreenManager từ kv
        self.screen_manager = self.root.ids.screen_manager
        # thiết lập current ban đầu
        self.root.ids.screen_manager.current = "home_screen"
        self._last_screen = self.screen_manager.current
        # bind để theo dõi thay đổi màn hình và cập nhật lịch sử
        self.screen_manager.bind(current=self._on_current)

    def _on_current(self, instance, value):
        # trước khi cập nhật _last_screen, nếu _last_screen tồn tại và khác giá trị mới
        if self._last_screen and self._last_screen != value:
            self.screen_history.append(self._last_screen)
        self._last_screen = value
        # cập nhật title của top bar (tùy theo tên màn hình)
        try:
            title = value.replace("_", " ").title()
            self.root.ids.top_bar.title = title
        except Exception:
            pass

    def go_back(self, *args):
        # nếu còn lịch sử thì lấy màn hình trước nhất và chuyển tới đó
        if self.screen_history:
            prev = self.screen_history.pop()
            self.screen_manager.current = prev
        else:
            # nếu không có lịch sử, về home (hoặc thoát)
            self.screen_manager.current = "home_screen"

    def on_stop(self):
        self.db.close()


if __name__ == "__main__":
    MainApp().run()
