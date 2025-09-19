import json
import random

json_file = "questions.json"
with open(json_file, "r", encoding="utf-8") as f:
    questions_data: list[dict] = json.load(f)

def set_question(question: dict):
        """Hàm cập nhật câu hỏi và đáp án"""
        ans_keys = ["A", "B", "C", "D"]
        ans = []
        for key in ans_keys:
            ans.append((key, question[key]))
        random.shuffle(ans)


set_question(questions_data[0])