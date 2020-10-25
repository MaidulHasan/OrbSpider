import re
import time

import scrapy
from scrapy.loader import ItemLoader
from scrapy.selector import Selector
from scrapy_selenium import SeleniumRequest
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from ..items import MalItem


""" -------- equivalent of normalize space function in xpath -------- """

def normalize_space(string):
    string = string.strip()
    string = re.sub(r'\s+', ' ', string)
    return string


class MalcompletedSpider(scrapy.Spider):
    name = 'MALCompleted'

    def start_requests(self):
        yield SeleniumRequest(
            url="https://www.myanimelist.net",
            callback=self.link_to_login_form,
            wait_time=10,
            wait_until=EC.element_to_be_clickable((By.ID, 'malLogin'))
        )

    def link_to_login_form(self, response):
        login_form = response.css("#malLogin::attr(href)").extract_first()
        yield SeleniumRequest(
            url=login_form,
            callback=self.login_n_navigate_n_parse
        )

    def login_n_navigate_n_parse(self, response):

        """ ---------- Logging in ---------- """

        driver = response.request.meta["driver"]
        username = driver.find_element_by_id("loginUserName")
        username.send_keys("********")  # Enter your Username
        password = driver.find_element_by_id("login-password")
        password.send_keys("*********")  # Enter your account Password
        password.send_keys(Keys.ENTER)

        """ ---------- Accepting Cookies -------- """
        try:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "div.button-wrapper button"))
            )
            driver.find_element_by_css_selector("div button").click()
        except:
            pass

        driver.implicitly_wait(5)

        """ --------- Navigating to the desired Page ---------- """
        # you can navigate to the page just by extracting the link and using SeleniumRequest/
        #  driver.get() but here we used this process just to demonstrate the process.
        # in case of using driver.get() bear in mind that selenium response object from driver doesn't work without
        # selenium commands
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".header-profile-link"))
            )
        except NoSuchElementException:
            raise Exception
        except ElementNotInteractableException:
            raise Exception

        driver.find_element_by_css_selector(".header-profile-link").click()

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".header-profile-dropdown li")))
        except NoSuchElementException:
            raise Exception
        except ElementNotInteractableException:
            raise Exception

        driver.find_elements_by_css_selector(".header-profile-dropdown li")[0].click()

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".anime.circle.completed")))
        except NoSuchElementException:
            raise Exception
        except ElementNotInteractableException:
            raise Exception

        driver.find_element_by_css_selector(".anime.circle.completed").click()

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "tbody.list-item")))
        except NoSuchElementException:
            raise Exception
        except ElementNotInteractableException:
            raise Exception

        driver.implicitly_wait(10)

        """ --------- Handling Infinite Scrolling --------- """

        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(5)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        # --important-- (used this because) selenium response object from driver doesn't work without selenium commands
        self.html = driver.page_source
        response = Selector(text=self.html)

        """ -------- Parsing Data -------- """

        animes = response.css("tbody.list-item")
        for anime in animes:
            loader = ItemLoader(item=MalItem(), selector=anime)
            i_url = anime.css("td.image img[src]::attr(src)").extract_first()
            rating = normalize_space(anime.css("td.score span::text").extract_first())
            loader.add_value("image_urls", i_url)
            loader.add_css("anime_title", "td.title > a::text")
            loader.add_value("personal_rating", rating)
            yield loader.load_item()
