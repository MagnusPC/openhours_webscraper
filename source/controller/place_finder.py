import sys
import time

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.mouse_button import MouseButton
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium.webdriver.common.by import By


class PlaceFinder:
    def search(self, query):
        driver = webdriver.Firefox()

        url = f"https://www.google.com/maps/search/{query.replace(' ', '+')}/"
        driver.get(url)

        # TODO refactor script
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

        # pass the cookie page
        time.sleep(2)
        cookie = driver.find_element(By.XPATH, '/html/body/c-wiz/div/div/div/div[2]/div[1]/div[3]'
                                               '/div[1]/div[1]/form[1]/div/div/button')
        cookie.click()

        # click out of search window
        mouse_tracker = driver.find_element(By.XPATH, '//*[@id="omnibox-singlebox"]')  # TODO fix it felix
        ActionChains(driver) \
            .move_to_element_with_offset(mouse_tracker, 0, 0) \
            .click(mouse_tracker) \
            .perform()

        # lists the first 7 hits, a scroll is needed to load more
        hits = []
        action = ActionChains(driver)

        while len(hits) < 1000:
            hits.append(driver.find_element(By.CLASS_NAME, 'hfpxzc'))
            action.scroll_to_element(hits[-1])
            # scroll_origin = ScrollOrigin.from_element(hits[len(hits) - 1])
            # action.scroll_from_origin(scroll_origin, 0, 1000).perform()
            # time.sleep(2)
            sys.stdout.write('.')  # a loading bar while waiting for the while loop to finish
            sys.stdout.flush()

        print(len(hits))

        urls = driver.execute_script(script)

        # driver.quit()

        return urls or [url]
