from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# Copy geckodriver to /var/bin

# driver = webdriver.Firefox(executable_path='/')
driver = webdriver.Firefox()
driver.get("http://www.mercante.transportes.gov.br/g36127/")
time.sleep(3)
elem = driver.find_element_by_link_text("aqui")
elem.click()
# driver.close()
