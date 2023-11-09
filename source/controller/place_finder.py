import sys
import time

import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.mouse_button import MouseButton
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
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


class PlaceFinder:
    def search(self, query):
        driver = webdriver.Firefox()
        # driver.fullscreen_window()
        url = f"https://www.google.com/maps/search/{query.replace(' ', '+')}/"

        try:
            driver.get(url)

            # pass the cookie page
            time.sleep(1)
            cookie = driver.find_element(By.XPATH, '/html/body/c-wiz/div/div/div/div[2]/div[1]/div[3]'
                                                   '/div[1]/div[1]/form[1]/div/div/button')
            cookie.click()

            # unclick search bar
            self.search_bar_unclicker(driver)

            # lists the first 7 hits, a scroll is needed to load more
            hits = []
            while len(hits) < 200:
                # hits.append(driver.find_elements(By.CLASS_NAME, 'Nv2PK.THOPZb.CpccDe'))
                found_elements = driver.find_elements(By.CLASS_NAME, 'hfpxzc')
                hits.extend(found_elements)
                if hits:
                    # TODO wait for next batch to load before continueing, instead of wait
                    action = ActionChains(driver)
                    bob = hits[-1].location_once_scrolled_into_view
                    action.scroll_to_element(hits[-1]).perform()
                    time.sleep(2)

                sys.stdout.write('.')  # a loading bar while waiting for the while loop to finish
                sys.stdout.flush()

            for hit in hits:
                print(f'\nGenbrug: {hit.accessible_name} med page id: {hit.id}')

            urls = driver.execute_script(wait_for_site_load())  # unused

            return urls or [url]
        except selenium.common.exceptions.MoveTargetOutOfBoundsException:
            driver.quit()

    def search_bar_unclicker(self, driver):
        mouse_tracker = driver.find_element(By.XPATH, '/html/body/div[3]/div[8]/div[9]/div/div/div[1]/div[2]/div/div['
                                                      '1]/div/div/div[1]/div[1]/div[6]')
        ActionChains(driver) \
            .move_to_element(mouse_tracker) \
            .click(mouse_tracker) \
            .perform()

        time.sleep(1)
