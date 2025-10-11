from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty


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

        user_data = {"name": name, "unit": unit, "score": 0}
            # do something with user_data, e.g. save or switch screen
        app.current_user = app.db.add_result(name, unit, 0)
        self.manager.current = "quiz_screen"
