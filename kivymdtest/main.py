import os

# Đảm bảo bạn đã cài đặt KivyMD 2.0.0
# pip install kivymd==2.0.0
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivy.core.window import Window

# (Tùy chọn) Đặt kích thước cửa sổ cho máy tính để bàn
Window.size = (350, 600)


# Định nghĩa các lớp Màn hình (Screens)
# Chúng ta chỉ cần định nghĩa chúng ở đây để Kivy có thể "thấy" chúng.
# Toàn bộ nội dung của chúng sẽ được định nghĩa trong file .kv
class Screen1(MDScreen):
    pass


class Screen2(MDScreen):
    pass


class Screen3(MDScreen):
    pass


# Định nghĩa Lớp màn hình chính chứa ScreenManager và NavigationBar
# Lớp này tương ứng với quy tắc <MainScreen> trong file .kv
class MainScreen(MDScreen):
    """
    Màn hình chính chứa ScreenManager và MDNavigationBar.
    """

    def on_item_select(
        self,
        instance_navigation_bar,
        instance_navigation_item,
    ) -> None:
        """
        Được gọi khi một mục trên thanh điều hướng được chọn.

        :param instance_navigation_bar: Thể hiện (instance) của MDNavigationBar
        :param instance_navigation_item: Thể hiện của MDNavigationItem được nhấn
        """
        # Lấy thuộc tính 'name' (tên) của mục được nhấn
        screen_name = instance_navigation_item.name

        # Sử dụng 'name' đó để chuyển màn hình hiện tại của ScreenManager
        # Chúng ta truy cập ScreenManager bằng 'id' của nó đã đặt trong file .kv
        self.ids.screen_manager.current = screen_name


class MainApp(MDApp):
    def build(self):
        # Thiết lập chủ đề (theme)
        self.theme_cls.theme_style = "Dark"  # "Light" or "Dark"
        self.theme_cls.primary_palette = "Blue"

        # Tải file Kivy (main.kv)
        # Tên file .kv phải khớp với tên lớp App (MainApp -> main.kv)
        # hoặc bạn có thể tải thủ công bằng Builder.load_file()
        return Builder.load_file("main.kv")


if __name__ == "__main__":
    # Đặt biến môi trường KIVY_TEXT=pil để render văn bản tốt hơn (tùy chọn)
    os.environ["KIVY_TEXT"] = "pil"
    MainApp().run()
