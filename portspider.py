from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Copy geckodriver to /var/bin

# driver = webdriver.Firefox(executable_path='/')
driver = webdriver.Firefox()
driver.get("http://www.mercante.transportes.gov.br/g36127/servlet/serpro.siscomex.mercante.servlet.MercanteController")

elem = driver.find_element_by_class_name("a2")


# driver.close()
