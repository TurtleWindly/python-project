from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.properties import ObjectProperty

from app.user import User


class RegisterScreen(MDScreen):
    name = "quiz_register_screen"

    # expose the id widgets to python if you want to access them via attributes
    name_text = ObjectProperty(None)
    unit_text = ObjectProperty(None)

    # prefer a clearer method name, but reg is fine
    def register_user(self):
        app = MDApp.get_running_app()
        name: str = self.name_text.text
        unit: str = self.unit_text.text

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
