import os
from source.controller.place_finder import PlaceFinder

# os.chdir(os.path.abspath(os.path.join("..", "..") + "\\"))
webscraper_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
os.chdir(webscraper_dir)
print("[" + webscraper_dir + "]")


# finding places
print(f'multi search: {PlaceFinder().search("genbrug aalborg")}')


# toodles
main_link = 'https://www.google.com/maps/search/genbrug+aalborg/'
# TODO remove 'tøjcontainer'
# TODO make nice ui