from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select

# from selenium.webdriver.support.ui import WebDriverWait
import time

# Copy geckodriver to /var/bin

portcall_sample_value = "20000350812"
# driver = webdriver.Firefox(executable_path='/')
driver = webdriver.Firefox()
driver.set_page_load_timeout(6)  # When to try again and reload.
driver.get("http://www.mercante.transportes.gov.br/g36127/")
time.sleep(2)

elem = driver.find_element_by_link_text("aqui")
elem.click()
time.sleep(2)

frame_select = driver.find_element_by_name("header")
driver.switch_to.frame(frame_select)
select1 = Select(driver.find_element_by_tag_name("select"))
select1_option = select1.select_by_visible_text("Consultar")

driver.switch_to.default_content()
frame_portcall_form = driver.find_element_by_id("Principal")
driver.switch_to.frame(frame_portcall_form)
elem = driver.find_element_by_name("NumEscala")
elem.clear()
elem.send_keys(portcall_sample_value)
elem.send_keys(Keys.RETURN)

time.sleep(6)
driver.close()
