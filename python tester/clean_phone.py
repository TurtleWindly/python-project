def clean_phone(phone):
    phone = str(phone)
    if phone[0] != "0":
        phone = "0" + phone
    return phone

print(clean_phone("092847"))