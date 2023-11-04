import os
# from bs4 import BeautifulSoup
# from selenium.webdriver import ActionChains
# from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
# from selenium.webdriver.common.by import By
from source.controller.place_finder import PlaceFinder

# os.chdir(os.path.abspath(os.path.join("..", "..") + "\\"))
webscraper_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
os.chdir(webscraper_dir)
print("[" + webscraper_dir + "]")


# finding places TODO make nice ui
print(f'multi search: {PlaceFinder().search("genbrug aalborg")}')


# toodles
main_link = 'https://www.google.com/maps/search/genbrug+aalborg/'
# TODO remove 'tøjcontainer'

# # extracting with selenium https://youtu.be/aZ45fzfyc8Q
# browser = webdriver.Firefox()
# record = []
# le = 0
#
# def Sel_extract():
#     action = ActionChains(browser)
#     a = browser.find_element(By.CLASS_NAME, 'hfpxzc')
#
#     while len(a) < 1000:
#         print(len(a))
#         var = len(a)
#         scroll_origin = ScrollOrigin.from_element(a[len(a)-1])  # var?
#         action.scroll_from_origin(scroll_origin, 0, 1000).perform()
#         time.sleep(2)
#         a = browser.find_element(By.CLASS_NAME, 'hfpxzc')  # dup?

# # Test project https://youtu.be/XVv6mJpFOb0
# page = requests.get('https://www.google.com/maps/search/genbrug+aalborg/@57.0276443,9.8316332,12z?entry=ttu').text
# soup = BeautifulSoup(page, 'lxml')
# hits = soup.find_all('div', class_='Nv2PK THOPZb CpccDe ')
# print(hits)

# with open(webscraper_dir + '/data/test-page.html', 'r') as html_file:
#     content = html_file.read()
#
#     soup = BeautifulSoup(content, 'lxml')
#     carousel_tags = soup.find_all('div', class_='wrapper')
#     for img in carousel_tags:
#         # print(car.img)
#         img_src = img.text.split()[-4:-2]
#         print(img_src)
