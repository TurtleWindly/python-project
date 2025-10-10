from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty


class RegisterScreen(Screen):
    name = "quiz_register_screen"

    # expose the id widgets to python if you want to access them via attributes
    name_text = ObjectProperty(None)
    unit_text = ObjectProperty(None)

    # prefer a clearer method name, but reg is fine
    def register_user(self):
        name = self.name_text.text_input.text
        unit = self.unit_text.text_input.text

        if name and unit:
            user_data = {"name": name, "unit": unit, "score": 0}
            # do something with user_data, e.g. save or switch screen
        print(name, unit)
