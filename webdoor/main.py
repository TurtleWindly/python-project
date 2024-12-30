import re
import requests
import os
from bs4 import BeautifulSoup

base_url = "https://cuanhuaangiaphat.com/"
product_url = "https://cuanhuaangiaphat.com/san-pham.html&p="
image_url = "https://cuanhuaangiaphat.com/upload/sanpham/"
images_folder = os.getcwd() + "/images/"


def extract_filename(path):
    # Biểu thức chính quy để lấy phần sau 'thumb/275x295/2/upload/sanpham/'
    pattern = r'thumb/275x295/2/upload/sanpham/(.+)'
    match = re.search(pattern, path)
    if match:
        return match.group(1)
    return None  # Trả về None nếu không tìm thấy


links = list()

for page in range(1, 23):
    product_list_html = requests.get(product_url + str(page))
    soup = BeautifulSoup(product_list_html.text, "html.parser")
    links += [img["src"] for img in soup.select(".item .sp_img a img")]


for link in links:
    try:
        response = requests.get(image_url + extract_filename(link))
        file_path = images_folder + extract_filename(link)

        with open(file_path, "wb") as fp:
            fp.write(response.content)

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
