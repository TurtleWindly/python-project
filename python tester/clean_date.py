from datetime import datetime

def clean_date(date: str):
    try:
        return datetime.strptime(date, "%d/%m/%Y")
    except ValueError:
        return datetime.strptime(date, "%m/%d/%Y")

print(clean_date("2/13/2023"))