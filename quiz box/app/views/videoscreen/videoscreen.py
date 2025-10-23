import os
import sys
import subprocess
from pathlib import Path

from kivy.utils import platform as kivy_platform
from kivy.properties import ObjectProperty
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.fitimage import FitImage
from kivy.metrics import dp

VIDEO_FOLDER = Path.cwd() / "res" / "videos"
THUMB_FOLDER = VIDEO_FOLDER / "thumbs"
PLACEHOLDER = VIDEO_FOLDER / "placeholder.png"  # provide placeholder.png in res/videos


class VideoScreen(MDScreen):
    """Màn hình hiển thị danh sách các video dưới dạng card với thumbnail"""
    name = "video_screen"
    video_list = ObjectProperty(None)

    def on_enter(self, *args):
        self.refresh_list()

    def open_file(self, path):
        """Mở file bằng ứng dụng mặc định của hệ điều hành."""
        # Android: dùng Intent, Desktop: dùng os.startfile / xdg-open
        if kivy_platform == "android":
            try:
                from jnius import autoclass, cast
                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                Intent = autoclass('android.content.Intent')
                Uri = autoclass('android.net.Uri')
                File = autoclass('java.io.File')
                FileProvider = autoclass('androidx.core.content.FileProvider')
                ctx = PythonActivity.mActivity
                file = File(str(path))
                uri = FileProvider.getUriForFile(ctx, ctx.getPackageName() + ".fileprovider", file)
                intent = Intent(Intent.ACTION_VIEW)
                intent.setDataAndType(uri, "video/*")
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

    def _ensure_thumb(self, video_path: Path) -> Path:
        """Tạo thumbnail cho video.
        - Android: dùng MediaMetadataRetriever qua pyjnius.
        - Khác: fallback trả placeholder (không tạo thumbnail bằng ffmpeg).
        Trả về Path của thumbnail nếu có, hoặc None.
        """
        THUMB_FOLDER.mkdir(parents=True, exist_ok=True)
        thumb_path = THUMB_FOLDER / (video_path.stem + ".png")
        if thumb_path.exists():
            return thumb_path

        # Android: dùng MediaMetadataRetriever
        if kivy_platform == "android":
            try:
                from jnius import autoclass
                MediaMetadataRetriever = autoclass('android.media.MediaMetadataRetriever')
                FileOutputStream = autoclass('java.io.FileOutputStream')
                BitmapCompressFormat = autoclass('android.graphics.Bitmap$CompressFormat')

                retriever = MediaMetadataRetriever()
                # setDataSource bằng đường dẫn file
                retriever.setDataSource(str(video_path))
                # lấy frame tại 1s (microsecond)
                bmp = retriever.getFrameAtTime(1000000)
                if bmp:
                    fos = FileOutputStream(str(thumb_path))
                    bmp.compress(BitmapCompressFormat.PNG, 100, fos)
                    fos.close()
                    retriever.release()
                    return thumb_path
                retriever.release()
            except Exception:
                # không phá vỡ chương trình nếu lỗi; fallback bên dưới
                pass

        # Fallback: nếu có placeholder thì dùng, còn không trả None
        if Path(PLACEHOLDER).exists():
            return Path(PLACEHOLDER)
        return None

    def refresh_list(self):
        """Làm mới danh sách card video."""
        container = self.ids.video_list
        container.clear_widgets()

        if not VIDEO_FOLDER.exists():
            container.add_widget(MDLabel(text="Thư mục video không tồn tại"))
            return

        video_files = [f for f in VIDEO_FOLDER.iterdir() if f.suffix.lower() == ".mp4"]

        if not video_files:
            container.add_widget(MDLabel(text="Không tìm thấy file video nào"))
            return

        for video_path in sorted(video_files):
            thumb = self._ensure_thumb(video_path)
            card = MDCard(
                size_hint=(None, None),
                size=(dp(180), dp(140)),
                elevation=4,
                radius=[8],
                ripple_behavior=True,
            )

            if thumb:
                img = FitImage(source=str(thumb), size_hint_y=0.75)
            else:
                img = FitImage(source="", size_hint_y=0.75)

            label = MDLabel(
                text=video_path.name,
                size_hint_y=0.25,
                halign="center",
                shorten=True,
                shorten_from="right",
                theme_text_color="Primary",
            )

            card.add_widget(img)
            card.add_widget(label)

            # TODO: Replace on touch up with proper button behavior
            def _on_touch_up(inst, touch, vp=video_path):
                if inst.collide_point(*touch.pos):
                    self.open_file(vp)

            card.bind(on_touch_up=_on_touch_up)

            container.add_widget(card)
