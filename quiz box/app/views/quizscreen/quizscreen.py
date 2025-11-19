import random
from kivy.app import App
from kivymd.uix.button import MDRectangleFlatButton as Button
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCardSwipe
from kivymd.uix.screen import MDScreen
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty, NumericProperty


class AnswerButton(Button):
    """Custom Button để lưu thông tin đáp án"""

    is_correct = BooleanProperty(False)  # Property để đánh dấu đáp án đúng
    tag = StringProperty("")  # Property để lưu nhãn đáp án (answer, option1, ...)


class SwipeToEditCard(MDCardSwipe):
    question_text = StringProperty("")
    question_id = StringProperty("")


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


class AddQuizScreen(MDScreen):
    name = "add_quiz_screen"

    def add_quiz(self):
        app = App.get_running_app()
        question_text: str = self.ids.question_text.text
        input_form = [
            self.ids.answer_text.text,
            self.ids.option1_text.text,
            self.ids.option2_text.text,
            self.ids.option3_text.text,
        ]
        if question_text == "":
            print("Question cannot be empty.")
            return
        for item in input_form:
            if item == "":
                print("All answer options must be filled.")
                return

        new_question = {
            "question": question_text.strip(),
            "answer": self.ids.answer_text.text,
            "option1": self.ids.option1_text.text,
            "option2": self.ids.option2_text.text,
            "option3": self.ids.option3_text.text,
        }
        app.question_manager.add(new_question)
        app.root.ids.screen_manager.current = "home_screen"


class ListQuizScreen(MDScreen):
    name = "list_quiz_screen"

    def on_enter(self):
        app = App.get_running_app()
        question_manager = app.question_manager
        quiz_list = self.ids.quiz_list
        quiz_list.clear_widgets()

        for question in question_manager.get_all():
            card = SwipeToEditCard(
                question_text=question["question"],
                question_id=str(question["id"]),
            )
            quiz_list.add_widget(card)

    def delete_question(self, qid: str):
        app = App.get_running_app()
        question_manager = app.question_manager
        question_manager.delete(int(qid))
        self.on_enter()  # Refresh the list

    def edit_quiz(self, qid: str):
        app = App.get_running_app()
        question = app.question_manager.get_by_id(int(qid))
        if question:
            edit_screen = app.root.ids.screen_manager.get_screen("edit_quiz_screen")
            edit_screen.question_id = question["id"]
            edit_screen.ids.question_text.text = question["question"]
            edit_screen.ids.answer_text.text = question["answer"]
            edit_screen.ids.option1_text.text = question["option1"]
            edit_screen.ids.option2_text.text = question["option2"]
            edit_screen.ids.option3_text.text = question["option3"]
            app.root.ids.screen_manager.current = "edit_quiz_screen"


class EditQuizScreen(MDScreen):
    name = "edit_quiz_screen"
    question_id = NumericProperty(0)

    def edit_quiz(self):
        app = App.get_running_app()
        question_text: str = self.ids.question_text.text
        input_form = [
            self.ids.answer_text.text,
            self.ids.option1_text.text,
            self.ids.option2_text.text,
            self.ids.option3_text.text,
        ]
        if question_text == "":
            print("Question cannot be empty.")
            return
        for item in input_form:
            if item == "":
                print("All answer options must be filled.")
                return

        new_question = {
            "question": question_text.strip(),
            "answer": self.ids.answer_text.text,
            "option1": self.ids.option1_text.text,
            "option2": self.ids.option2_text.text,
            "option3": self.ids.option3_text.text,
        }
        app.question_manager.update(self.question_id, new_question)
        app.root.ids.screen_manager.current = "list_quiz_screen"
