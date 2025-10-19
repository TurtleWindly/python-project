import os
import shutil
import sys
import subprocess
from pathlib import Path
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics.texture import Texture
from kivymd.uix.screen import MDScreen
from kivy.uix.button import Button
from kivy.uix.label import Label

VIDEO_FOLDER = Path.cwd() / "res" / "videos"


class VideoScreen(MDScreen):
    """Màn hình hiển thị danh sách các video"""

    name = "video_screen"

    def on_enter(self, *args):
        self.refresh_list()

    def open_file(self, path):
        """Mở file bằng ứng dụng mặc định của hệ điều hành."""
        if os.name == "nt":  # Windows
            os.startfile(path)
        elif sys.platform.startswith("darwin"):  # macOS
            subprocess.call(("open", path))
        elif os.name == "posix":  # Linux/Unix
            subprocess.call(("xdg-open", path))

    def refresh_list(self):
        """Làm mới danh sách các file video hiển thị."""
        files_box = self.ids.files_box
        files_box.clear_widgets()

        video_files = [f for f in os.listdir(VIDEO_FOLDER) if f.lower().endswith(".mp4")]

        if not video_files:
            files_box.add_widget(Label(text="Không tìm thấy file video nào"))
        else:
            for f in video_files:
                btn = Button(text=f, size_hint_y=None, height=50)
                btn.bind(
                    on_release=lambda inst, filename=f: self.open_file(
                        VIDEO_FOLDER / filename
                    )
                )
                files_box.add_widget(btn)
