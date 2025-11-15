import json
import random
from kivymd.uix.button import MDRectangleFlatButton as Button
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.screen import MDScreen
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty


class AnswerButton(Button):
    """Custom Button để lưu thông tin đáp án"""

    is_correct = BooleanProperty(False)  # Property để đánh dấu đáp án đúng
    tag = StringProperty("")  # Property để lưu nhãn đáp án (answer, option1, ...)


class QuizBox(MDBoxLayout):
    # Khai báo property để bind tới button trong KV
    question_label = ObjectProperty(None)
    answer_btn1 = ObjectProperty(None)
    answer_btn2 = ObjectProperty(None)
    answer_btn3 = ObjectProperty(None)
    answer_btn4 = ObjectProperty(None)

    def set_question(self, question: dict, question_data: list[dict]):
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
        ans_keys = ["answer", "option1", "option2", "option3"]
        ans = []
        for key in ans_keys:
            ans.append((key, question[key]))
        random.shuffle(ans)

        # Cập nhật text và tag cho từng button
        for index, (key, value) in enumerate(ans):
            buttons[index].text = value
            buttons[index].tag = key
            buttons[index].is_correct = True if key == "answer" else False

        # Remove used question from the list
        question_data.remove(question)

    def check_answer(self, app: MDApp, selected_answer, questions_data: list[dict]):
        """Hàm kiểm tra đáp án"""
        app.current_user.score += 1 if selected_answer else 0
        self.parent.answered_question += 1

        # Check if quiz is over
        if self.parent.answered_question >= app.settings.max_question:
            app.db.add_result(
                app.current_user.name, app.current_user.unit, app.current_user.score
            )
            # Reset quiz state
            self.parent.answered_question = 0
            app.root.ids.screen_manager.current = "result_screen"
            return

        if selected_answer:
            self.set_question(random.choice(questions_data), questions_data)
        else:
            # TODO: Popup thông báo sai 1s rồi tự đóng
            print("Sai rồi!")
            self.set_question(random.choice(questions_data), questions_data)


class QuizScreen(MDScreen):
    name = "quiz_screen"
    quizbox = ObjectProperty(None)
    answered_question = 0
    questions_data: list[dict]

    def __init__(self, **kw):
        super().__init__(**kw)
        self.app = MDApp.get_running_app()
        self._bound = False  # tránh bind nhiều lần

    def _on_answer(self, btn):
        # handler chung cho tất cả button
        self.quizbox.check_answer(self.app, btn.is_correct, self.questions_data)

    def on_enter(self):
        self.questions_data = self.app.question_manager.get_all().copy()
        self.quizbox.set_question(
            random.choice(self.questions_data), self.questions_data
        )

        # bind chỉ một lần
        if not self._bound:
            self.quizbox.answer_btn1.bind(on_release=self._on_answer)
            self.quizbox.answer_btn2.bind(on_release=self._on_answer)
            self.quizbox.answer_btn3.bind(on_release=self._on_answer)
            self.quizbox.answer_btn4.bind(on_release=self._on_answer)
            self._bound = True
