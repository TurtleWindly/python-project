import json
import os


class AppSettings:
    """Class quản lý cài đặt ứng dụng (đọc/ghi JSON, giữ nguyên kiểu dữ liệu Python)."""

    def __init__(self, file_path="settings.json"):
        self.file_path = file_path

        # Các thuộc tính cài đặt mặc định
        self.max_question: int = 10
        self.volume: float = 1.0

        # Đọc từ file nếu có
        self.load()

    # ------------------------------------
    # Các hàm xử lý JSON
    # ------------------------------------
    def to_dict(self):
        """Chuyển object -> dict (để lưu JSON)."""
        return {
            "max_question": self.max_question,
            "volume": self.volume,
        }

    def from_dict(self, data: dict):
        """Đọc dict -> gán lại giá trị cho object."""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def save(self):
        """Lưu ra file JSON."""
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=4)

    def load(self):
        """Đọc file JSON (nếu có) và phục hồi cài đặt."""
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.from_dict(data)
            except Exception as e:
                print(f"⚠️ Lỗi khi đọc file cài đặt: {e}. Dùng giá trị mặc định.")
                self.save()  # tạo file mới

    def reset_defaults(self):
        """Khôi phục giá trị mặc định."""
        self.__init__(self.file_path)
        self.save()
