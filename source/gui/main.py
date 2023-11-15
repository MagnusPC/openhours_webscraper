import os
from source.controller.place_finder import search

# os.chdir(os.path.abspath(os.path.join("..", "..") + "\\"))
webscraper_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
os.chdir(webscraper_dir)
print("[" + webscraper_dir + "]")

# finding places
print(f'multi search: {search("genbrug aalborg", "tøjcontainer")}')

# toodles
main_url = 'https://www.google.com/maps/search/genbrug+aalborg/'
# TODO make nice ui
# TODO data analysis, connect with gui?
