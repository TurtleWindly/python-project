def hoten(full_name, get_first_name):
    names = full_name.split()
    if get_first_name:
        return names[-1]
    else:
        return " ".join(names[:-1])


def test_hoten(name):
    print(hoten(name, True))  # sẽ in ra "Duy"
    print(hoten(name, False))  # sẽ in ra "Nguyễn Phúc"


# Ví dụ sử dụng
test_hoten("Nguyễn Phúc Duy")
test_hoten("Quách Hữu Cảnh Cao")
test_hoten("Mạnh Trường")
test_hoten("Giường")
