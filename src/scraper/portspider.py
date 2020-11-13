from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.firefox.options import Options

from bs4 import BeautifulSoup

# from selenium.webdriver.support.ui import WebDriverWait
import time

portcall_sample_value = "20000350812"


def driver_setup():
    options = Options()
    driver = webdriver.PhantomJS()
    driver.set_page_load_timeout(20)  # When to try again and reload.
    return driver


def reach_main_page(driver):
    driver.get("http://www.mercante.transportes.gov.br/g36127/")
    time.sleep(2)


def select_consult_option(driver):
    frame_select = driver.find_element_by_name("header")
    driver.switch_to.frame(frame_select)
    select1 = Select(driver.find_element_by_tag_name("select"))
    select1_option = select1.select_by_visible_text("Consultar")


def go_to_form_page(driver):
    elem = driver.find_element_by_link_text("aqui")
    elem.click()
    time.sleep(2)


def do_portcall_search(driver):
    frame_portcall_form = driver.find_element_by_id("Principal")
    driver.switch_to.frame(frame_portcall_form)
    elem = driver.find_element_by_name("NumEscala")
    elem.clear()
    elem.send_keys(portcall_sample_value)
    elem.send_keys(Keys.RETURN)


def end_driver(driver):
    time.sleep(6)
    driver.close()


# Copy geckodriver to /var/bin

driver = driver_setup()

reach_main_page(driver)

go_to_form_page(driver)

select_consult_option(driver)

driver.switch_to.default_content()

do_portcall_search(driver)

soup = BeautifulSoup(driver.page_source)

print(soup)

end_driver(driver)