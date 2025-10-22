import os
import shutil
import sys
import subprocess
from pathlib import Path

from kivy.properties import ObjectProperty
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import MDList, OneLineListItem
from kivy.uix.button import Button
from kivymd.uix.label import MDLabel

VIDEO_FOLDER = Path.cwd() / "res" / "videos"


class VideoScreen(MDScreen):
    """Màn hình hiển thị danh sách các video"""
    name = "video_screen"
    video_list = ObjectProperty(None)

    def on_enter(self, *args):
        print("Entering Video Screen")
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
        video_list = self.ids.video_list
        video_list.clear_widgets()

        video_files = [f for f in os.listdir(VIDEO_FOLDER) if f.lower().endswith(".mp4")]

        if not video_files:
            video_list.add_widget(MDLabel(text="Không tìm thấy file video nào"))
        else:
            for f in video_files:
                list_item = OneLineListItem(text=f)
                list_item.bind(
                    on_release=lambda inst, filename=f: self.open_file(
                        VIDEO_FOLDER / filename
                    )
                )
                video_list.add_widget(list_item)
