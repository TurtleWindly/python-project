import json
import random
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty

number_of_questions = 10
grade = 0

json_file = "questions.json"
with open(json_file, "r", encoding="utf-8") as f:
    questions_data: list[dict] = json.load(f)


class AnswerButton(Button):
    """Custom Button để lưu thông tin đáp án"""

    is_correct = BooleanProperty(False)  # Property để đánh dấu đáp án đúng
    tag = StringProperty("")  # Property để lưu nhãn đáp án (A, B, C, D)


class QuizBox(BoxLayout):
    # Khai báo property để bind tới button trong KV
    question_label = ObjectProperty(None)
    answer_btn1 = ObjectProperty(None)
    answer_btn2 = ObjectProperty(None)
    answer_btn3 = ObjectProperty(None)
    answer_btn4 = ObjectProperty(None)

    def set_question(self, question: dict):
        """Hàm cập nhật câu hỏi và đáp án"""
        # Lưu các button vào một list để dễ thao tác
        buttons = [
            self.answer_btn1,
            self.answer_btn2,
            self.answer_btn3,
            self.answer_btn4,
        ]
        # Cập nhật câu hỏi
        self.question_label.text = question["question"]
        # Tạo list đáp án và xáo trộn
        ans_keys = ["A", "B", "C", "D"]
        ans = []
        for key in ans_keys:
            ans.append((key, question[key]))
        random.shuffle(ans)

        # Cập nhật text và tag cho từng button
        for index, (key, value) in enumerate(ans):
            buttons[index].text = value
            buttons[index].tag = key
            buttons[index].is_correct = True if key == question["answer"] else False

    def check_answer(self, app: App, selected_answer):
        """Hàm kiểm tra đáp án"""
        app.current_user.score += 1 if selected_answer else 0
        self.parent.answered_question += 1
        print("Answered: " + str(self.parent.answered_question))
        print("Score: " + str(app.current_user.score))

        if self.parent.answered_question >= app.settings.max_question:
            print(f"Chúc mừng {app.current_user.name}, bạn đã hoàn thành bài quiz!")
            result = app.db.add_result(
                app.current_user.name, app.current_user.unit, app.current_user.score
            )
            app.root.current = "result_screen"

        if selected_answer:
            self.set_question(random.choice(questions_data))
        else:
            # TODO: Popup thông báo sai 1s rồi tự đóng
            print("Sai rồi!")
            self.set_question(random.choice(questions_data))

    def reset_quiz(self):
        """Hàm đặt lại câu hỏi mới"""
        new_question = random.choice(questions_data)
        self.set_question(new_question)


class QuizScreen(Screen):
    name = "quiz_screen"
    quizbox = ObjectProperty(None)
    answered_question = 0

    def __init__(self, **kw):
        super().__init__(**kw)
        self.app = App.get_running_app()

    def on_enter(self):
        self.quizbox.set_question(questions_data[0])
        self.quizbox.answer_btn1.bind(
            on_release=lambda btn: self.quizbox.check_answer(self.app, btn.is_correct)
        )
        self.quizbox.answer_btn2.bind(
            on_release=lambda btn: self.quizbox.check_answer(self.app, btn.is_correct)
        )
        self.quizbox.answer_btn3.bind(
            on_release=lambda btn: self.quizbox.check_answer(self.app, btn.is_correct)
        )
        self.quizbox.answer_btn4.bind(
            on_release=lambda btn: self.quizbox.check_answer(self.app, btn.is_correct)
        )
