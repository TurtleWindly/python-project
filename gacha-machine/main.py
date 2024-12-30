import PySimpleGUI as sg
import random
import json

from enum import Enum


class Ratio:
    def __init__(self, break_point: int = 25, rate: float = 1) -> None:
        self.break_point = break_point
        self.rate = rate


class ItemType(Enum):
    Weapon = 1
    Character = 2


class Item:
    def __init__(
        self,
        drop_rate: float,
        start: int = 3,
        item_type: ItemType = ItemType.Weapon,
        name: str = "No name",
    ):
        self.drop_rate = drop_rate
        self.start = start
        self.item_type = item_type
        self.name = name

    def __repr__(self):
        return f"{self.name}"


def weighted_random_choice(items, insurance, break_point, banner):
    total = sum(item.drop_rate for item in items)
    r = random.uniform(0, total)
    upto = 0
    print(f"Bảo hiểm: {insurance}")
    for item in items:
        if item.name == banner:
            for ratio in break_point:
                if insurance >= ratio.break_point:
                    item.drop_rate = item.drop_rate + ratio.rate
                    print(f"{item.name} drop: {item.drop_rate}")
    for item in items:
        if upto + item.drop_rate >= r:
            return item
        upto += item.drop_rate


# Đọc dữ liệu từ file JSON
with open("data.json", "r") as file:
    data = json.load(file)

# Chuyển đổi dữ liệu thành danh sách các đối tượng Item
items = [Item(**item) for item in data]

# Bao hiem
insurance = 0
break_point = [Ratio(75, 1)]
banner = "Diluc"

# In danh sách các đối tượng Item
# for item in items:
#     print(item)


# All the stuff inside your window.
layout = [[sg.Text("Banner Diluc")], [sg.Button("1 time"), sg.Button("10 times")]]

# Create the Window
window = sg.Window("Genshin killer", layout)

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()

    # if user closes window or clicks cancel
    if event == sg.WIN_CLOSED or event == "Cancel":
        break

    if event == "1 time":
        output = f"{weighted_random_choice(items, insurance, break_point, banner)}"
        if output != banner:
            insurance += 1
        elif output == banner:
            insurance = 0
        sg.popup(output)

    if event == "10 times":
        result = []
        kq = "Chúc mừng nhận: "
        for _ in range(10):
            output = weighted_random_choice(items, insurance, break_point, banner)
            if output.name != banner:
                insurance += 1
            elif output.name == banner:
                insurance = 0
            result.append(output)
        for vat_pham in result:
            kq += f"{vat_pham} "
        sg.popup(kq)


window.close()
