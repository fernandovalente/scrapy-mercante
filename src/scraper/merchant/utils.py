from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
import time


def driver_setup():
    driver = webdriver.Chrome(
        "/home/jaxe/Documents/repositorios/portmarket/scrapy-mercante/chromedriver_linux64/chromedriver"
    )
    driver.set_page_load_timeout(6)  # When to try again and reload.
    return driver


def reach_main_page(driver):
    driver.get("http://www.mercante.transportes.gov.br/g36127/")
    time.sleep(3)


def select_consult_option(driver):
    frame_select = driver.find_element_by_name("header")
    driver.switch_to.frame(frame_select)
    select1 = Select(driver.find_element_by_tag_name("select"))
    select1_option = select1.select_by_visible_text("Consultar")


def go_to_search_main_page(driver):
    elem = driver.find_element_by_link_text("aqui")
    elem.click()
    time.sleep(2)


def do_portcall_search(driver, portcall_value):
    frame_portcall_form = driver.find_element_by_id("Principal")
    driver.switch_to.frame(frame_portcall_form)
    elem = driver.find_element_by_name("NumEscala")
    elem.clear()
    elem.send_keys(portcall_value)
    elem.send_keys(Keys.RETURN)


def end_driver(driver):
    time.sleep(6)
    driver.close()
