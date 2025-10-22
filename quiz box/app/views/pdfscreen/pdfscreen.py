import os
import shutil
import sys
import subprocess
from pathlib import Path

from kivy.utils import platform as kivy_platform
from kivy.uix.screenmanager import Screen
from plyer import filechooser

from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.fitimage import FitImage
from kivy.metrics import dp

PDF_FOLDER = Path.cwd() / "res" / "pdf"
THUMB_FOLDER = PDF_FOLDER / "thumbs"
PLACEHOLDER = PDF_FOLDER / "placeholder.png"  # optional placeholder.png in res/pdf


class PdfScreen(Screen):
    """Màn hình hiển thị danh sách các file PDF dưới dạng card với thumbnail"""

    name = "pdf_screen"

    def on_enter(self, *args):
        PDF_FOLDER.mkdir(parents=True, exist_ok=True)
        THUMB_FOLDER.mkdir(parents=True, exist_ok=True)
        self.refresh_list()

    def open_pdf(self, path):
        """Mở file PDF bằng ứng dụng mặc định của hệ điều hành."""
        if kivy_platform == "android":
            try:
                # Dùng intent để mở file trên Android
                from jnius import autoclass
                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                Intent = autoclass('android.content.Intent')
                Uri = autoclass('android.net.Uri')
                File = autoclass('java.io.File')
                FileProvider = autoclass('androidx.core.content.FileProvider')
                ctx = PythonActivity.mActivity
                file = File(str(path))
                uri = FileProvider.getUriForFile(ctx, ctx.getPackageName() + ".fileprovider", file)
                intent = Intent(Intent.ACTION_VIEW)
                intent.setDataAndType(uri, "application/pdf")
                intent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
                ctx.startActivity(intent)
                return
            except Exception:
                pass

        if os.name == "nt":  # Windows
            os.startfile(str(path))
        elif sys.platform.startswith("darwin"):  # macOS
            subprocess.call(("open", str(path)))
        elif os.name == "posix":  # Linux/Unix
            subprocess.call(("xdg-open", str(path)))

    def _ensure_thumb(self, pdf_path: Path) -> Path:
        """Tạo/ lấy thumbnail cho PDF.
        - Android: dùng PdfRenderer qua pyjnius (API 21+).
        - Desktop: dùng PyMuPDF (fitz) nếu có.
        - Fallback: placeholder nếu không thể render.
        Trả về Path tới thumbnail (png) hoặc None.
        """
        THUMB_FOLDER.mkdir(parents=True, exist_ok=True)
        thumb_path = THUMB_FOLDER / (pdf_path.stem + ".png")
        if thumb_path.exists():
            return thumb_path

        # Android: PdfRenderer
        if kivy_platform == "android":
            try:
                from jnius import autoclass, cast
                ParcelFileDescriptor = autoclass('android.os.ParcelFileDescriptor')
                PdfRenderer = autoclass('android.graphics.pdf.PdfRenderer')
                File = autoclass('java.io.File')
                Bitmap = autoclass('android.graphics.Bitmap')
                FileOutputStream = autoclass('java.io.FileOutputStream')
                BitmapCompressFormat = autoclass('android.graphics.Bitmap$CompressFormat')

                file = File(str(pdf_path))
                pfd = ParcelFileDescriptor.open(file, ParcelFileDescriptor.MODE_READ_ONLY)
                renderer = PdfRenderer(pfd)
                if renderer.getPageCount() > 0:
                    page = renderer.openPage(0)
                    width = page.getWidth()
                    height = page.getHeight()
                    bmp = Bitmap.createBitmap(width, height, Bitmap.Config.ARGB_8888)
                    page.render(bmp, None, None, 1)
                    fos = FileOutputStream(str(thumb_path))
                    bmp.compress(BitmapCompressFormat.PNG, 100, fos)
                    fos.close()
                    page.close()
                    renderer.close()
                    pfd.close()
                    return thumb_path
            except Exception:
                pass

        # Desktop: try PyMuPDF (fitz)
        try:
            import fitz  # PyMuPDF
            doc = fitz.open(str(pdf_path))
            page = doc.load_page(0)
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # scale for better resolution
            pix.save(str(thumb_path))
            doc.close()
            if thumb_path.exists():
                return thumb_path
        except Exception:
            pass

        # fallback placeholder
        if Path(PLACEHOLDER).exists():
            return Path(PLACEHOLDER)
        return None

    def refresh_list(self):
        """Làm mới danh sách card PDF."""
        files_box = self.ids.files_box
        files_box.clear_widgets()

        pdf_files = sorted([f for f in PDF_FOLDER.iterdir() if f.suffix.lower() == ".pdf"])

        if not pdf_files:
            files_box.add_widget(MDLabel(text="Không tìm thấy file PDF nào", halign="center"))
            return

        for pdf in pdf_files:
            thumb = self._ensure_thumb(pdf)
            card = MDCard(
                size_hint=(None, None),
                size=(dp(180), dp(220)),
                elevation=4,
                radius=[8],
                ripple_behavior=True,
            )

            if thumb:
                img = FitImage(source=str(thumb), size_hint_y=0.85)
            else:
                img = FitImage(source="", size_hint_y=0.85)

            label = MDLabel(
                text=pdf.name,
                size_hint_y=0.15,
                halign="center",
                shorten=True,
                shorten_from="right",
                theme_text_color="Primary",
            )

            card.add_widget(img)
            card.add_widget(label)

            # TODO: Replace on touch up with proper button behavior
            def _on_touch_up(inst, touch, p=pdf):
                if inst.collide_point(*touch.pos):
                    self.open_pdf(p)

            card.bind(on_touch_up=_on_touch_up)
            files_box.add_widget(card)

    def pick_file(self):
        """Mở trình chọn file để người dùng chọn file PDF từ hệ thống và copy vào thư mục res/pdf."""
        paths = filechooser.open_file(title="Chọn file PDF", filters=["*.pdf"], multiple=False)
        if not paths:
            return
        src = paths[0]
        filename = os.path.basename(src)
        dest_path = PDF_FOLDER / filename
        try:
            PDF_FOLDER.mkdir(parents=True, exist_ok=True)
            shutil.copy(src, str(dest_path))
            # xóa thumbnail cũ nếu có để tái tạo
            t = THUMB_FOLDER / (Path(filename).stem + ".png")
            if t.exists():
                t.unlink()
            self.refresh_list()
            print(f"Đã lưu: {dest_path}")
        except Exception as e:
            print(f"Lỗi khi copy file: {e}")
