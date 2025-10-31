import json
import os


class QuestionManager:
    def __init__(self, filename: str):
        self.filename = filename
        self.questions = []
        self.load()

    def load(self):
        """Tải dữ liệu từ file JSON"""
        if os.path.exists(self.filename):
            with open(self.filename, "r", encoding="utf-8") as f:
                try:
                    self.questions = json.load(f)
                except json.JSONDecodeError:
                    self.questions = []
        else:
            self.questions = []
            self.save()  # tạo file trống nếu chưa có

    def save(self):
        """Lưu dữ liệu vào file JSON"""
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(self.questions, f, indent=2, ensure_ascii=False)

    def get_all(self):
        """Lấy toàn bộ danh sách câu hỏi"""
        return self.questions

    def get_by_id(self, qid: int):
        """Lấy câu hỏi theo ID"""
        for q in self.questions:
            if q["id"] == qid:
                return q
        return None

    def add(self, question_data: dict):
        """
        Thêm câu hỏi mới.
        Tự động tạo ID nếu không có trong dữ liệu.
        """
        if "id" not in question_data:
            next_id = max((q["id"] for q in self.questions), default=0) + 1
            question_data["id"] = next_id

        # kiểm tra trùng ID
        if any(q["id"] == question_data["id"] for q in self.questions):
            raise ValueError(f"ID {question_data['id']} đã tồn tại")

        self.questions.append(question_data)
        self.save()

    def update(self, qid: int, new_data: dict):
        """Cập nhật nội dung câu hỏi theo ID"""
        for q in self.questions:
            if q["id"] == qid:
                q.update(new_data)
                self.save()
                return True
        return False

    def delete(self, qid: int):
        """Xóa câu hỏi theo ID"""
        for q in self.questions:
            if q["id"] == qid:
                self.questions.remove(q)
                self.save()
                return True
        return False

    def find_by_keyword(self, keyword: str):
        """Tìm kiếm câu hỏi theo từ khóa"""
        keyword = keyword.lower()
        return [q for q in self.questions if keyword in q["question"].lower()]

    def clear(self):
        """Xóa toàn bộ dữ liệu"""
        self.questions = []
        self.save()
