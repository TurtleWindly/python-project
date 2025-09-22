import os
import shutil
import sys
import subprocess
from pathlib import Path
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics.texture import Texture
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from plyer import filechooser

PDF_FOLDER = Path.cwd() / "res" / "pdf"


class PdfScreen(Screen):
    """Màn hình hiển thị danh sách các file PDF"""

    name = "pdf_screen"

    def on_enter(self, *args):
        self.refresh_list()

    def open_pdf(self, path):
        """Mở file PDF bằng ứng dụng mặc định của hệ điều hành."""
        if os.name == "nt":  # Windows
            os.startfile(path)
        elif sys.platform.startswith("darwin"):  # macOS
            subprocess.call(("open", path))
        elif os.name == "posix":  # Linux/Unix
            subprocess.call(("xdg-open", path))

    def refresh_list(self):
        """Làm mới danh sách các file PDF hiển thị."""
        files_box = self.ids.files_box
        files_box.clear_widgets()

        pdf_files = [f for f in os.listdir(PDF_FOLDER) if f.lower().endswith(".pdf")]

        if not pdf_files:
            files_box.add_widget(Label(text="Không tìm thấy file PDF nào"))
        else:
            for f in pdf_files:
                btn = Button(text=f, size_hint_y=None, height=50)
                btn.bind(
                    on_release=lambda inst, filename=f: self.open_pdf(
                        PDF_FOLDER / filename
                    )
                )
                files_box.add_widget(btn)


    def pick_file(self):
        """Mở trình chọn file để người dùng chọn file PDF từ hệ thống."""
        file_path = filechooser.open_file(
            title="Chonjnnn", filters=["*.pdf"], mutiple=False
        )
        if file_path:
            src = file_path[0]
            filename = os.path.basename(src)
            dest = os.path.join(PDF_FOLDER, filename)
            print(filename, dest)

            try:
                shutil.copy(src, dest)  # copy file vào res/pdf
                self.refresh_list()
                # TODO: Logging here
                print(f"Đã lưu: {dest}")
            except Exception as e:
                print(f"Lỗi khi copy file:\n{e}")
