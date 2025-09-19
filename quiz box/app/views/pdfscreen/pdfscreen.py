import os
import sys
import subprocess
from pathlib import Path
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics.texture import Texture
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.label import Label

PDF_FOLDER = Path.cwd() / "res" / "pdf"


class PdfScreen(Screen):
    """Màn hình hiển thị danh sách các file PDF"""

    name = "pdf_screen"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical")

        if not os.path.exists(PDF_FOLDER):
            os.makedirs(PDF_FOLDER)

        pdf_files = [f for f in os.listdir(PDF_FOLDER) if f.lower().endswith(".pdf")]

        if not pdf_files:
            layout.add_widget(Label(text="Không tìm thấy file PDF nào"))
        else:
            for f in pdf_files:
                btn = Button(text=f, size_hint_y=None, height=50)
                btn.bind(
                    on_release=lambda inst, filename=f: self.open_pdf(
                        PDF_FOLDER / filename
                    )
                )
                layout.add_widget(btn)

        self.add_widget(layout)

    def open_pdf(self, path):
        """Mở file PDF bằng ứng dụng mặc định của hệ điều hành."""
        if os.name == "nt":  # Windows
            os.startfile(path)
        elif sys.platform.startswith("darwin"):  # macOS
            subprocess.call(("open", path))
        elif os.name == "posix":  # Linux/Unix
            subprocess.call(("xdg-open", path))


# TODO: Add pdf file to workspace of the app
class PdfChooser(Screen):
    pass
