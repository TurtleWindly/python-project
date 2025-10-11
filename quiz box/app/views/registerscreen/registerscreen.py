from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty

from app.user import User


class RegisterScreen(Screen):
    name = "quiz_register_screen"

    # expose the id widgets to python if you want to access them via attributes
    name_text = ObjectProperty(None)
    unit_text = ObjectProperty(None)

    # prefer a clearer method name, but reg is fine
    def register_user(self):
        app = App.get_running_app()
        name: str = self.name_text.text_input.text
        unit: str = self.unit_text.text_input.text

        if not name and not unit:
            # TODO: Create a popup to inform the user
            return

        name = name.strip()
        unit = unit.strip()

        if name == "" and unit == "":
            # TODO: Create a popup to inform the user
            return

        app.current_user = User(name=name, unit=unit, score=0)
        self.manager.current = "quiz_screen"
