from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# import ipdb; ipdb.set_trace()

driver = webdriver.Chrome()
driver.get("https://www.mercante.transportes.gov.br/g36127/html/Escala/EscalaConsul.html")

elem = driver.find_element_by_name("NumEscala")
