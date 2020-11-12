from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select

# from selenium.webdriver.support.ui import WebDriverWait
import time

# Copy geckodriver to /var/bin

# driver = webdriver.Firefox(executable_path='/')
driver = webdriver.Firefox()
driver.get("http://www.mercante.transportes.gov.br/g36127/")
time.sleep(3)
elem = driver.find_element_by_link_text("aqui")
elem.click()
time.sleep(3)

frame1 = driver.find_element_by_name("header")
driver.switch_to.frame(frame1)

select1 = Select(driver.find_element_by_tag_name("select"))
select1_option = select1.select_by_visible_text("Consultar")

time.sleep(10)
driver.close()
