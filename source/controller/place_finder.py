import sys
import time

import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By


def wait_for_site_load():
    script = """
        function waitCss(selector, n=1, require=false, timeout=5000) {
          console.log(selector, n, require, timeout);
          var start = Date.now();
          while (Date.now() - start < timeout){
            if (document.querySelectorAll(selector).length >= n){
              return document.querySelectorAll(selector);
            }
          }
          if (require){
              throw new Error(`selector "${selector}" timed out in ${Date.now() - start} ms`);
          } else {
              return document.querySelectorAll(selector);
          }
        }

        var results = waitCss("div[role*=article]>a", n=10, require=false);
        return Array.from(results).map((el) => el.getAttribute("href"))
        """
    return script


def element_remover(hits, str_to_remove):
    # remove duplicates
    sorted_hits = list(dict.fromkeys(hits))  # better to not collect duplicates

    # remove elements containing 'tøjcontainer'
    for element in sorted_hits:
        if element.accessible_name.find(str_to_remove) != -1:
            print(f'removed {element.accessible_name} with id {element.id}')
            sorted_hits.remove(element)  # somehow two always escape

    return sorted_hits


def search_bar_unclicker(driver):
    mouse_tracker = driver.find_element(By.XPATH, '/html/body/div[3]/div[8]/div[9]/div/div/div[1]/div[2]/div/div['
                                                  '1]/div/div/div[1]/div[1]/div[6]')
    ActionChains(driver) \
        .move_to_element(mouse_tracker) \
        .click(mouse_tracker) \
        .perform()

    time.sleep(1)


def search(query, word_to_avoid):
    driver = webdriver.Firefox()
    url = f"https://www.google.com/maps/search/{query.replace(' ', '+')}/"

    try:
        driver.get(url)

        # pass the cookie page
        time.sleep(1)
        cookie = driver.find_element(By.XPATH, '/html/body/c-wiz/div/div/div/div[2]/div[1]/div[3]'
                                               '/div[1]/div[1]/form[1]/div/div/button')
        cookie.click()

        # unclick search bar
        search_bar_unclicker(driver)

        # lists the first 7 hits, a scroll is needed to load more
        hits = []
        sys.stdout.write('Loading elements')
        # TODO change looping method, still sometimes breaks off at the end
        while len(hits) < 200:
            found_elements = driver.find_elements(By.CLASS_NAME, 'hfpxzc')
            hits.extend(found_elements)
            if hits:
                action = ActionChains(driver)
                bob = hits[-1].location_once_scrolled_into_view  # TODO look up
                action.scroll_to_element(hits[-1]).perform()
                time.sleep(2)  # TODO change to wait for next element to load

            sys.stdout.write('.')  # a loading bar while waiting for the while loop to finish
            sys.stdout.flush()

        sys.stdout.write('\n')  # add space after loading
        hits = element_remover(hits, word_to_avoid)

        # visualizer for collected data, TODO save as file instead, for data analysis
        for hit in hits:
            print(f'\nGenbrug: {hit.accessible_name} med page id: {hit.id}')

        urls = driver.execute_script(wait_for_site_load())  # unused

        driver.quit()

        return urls or [url]

    finally:
        driver.minimize_window()
