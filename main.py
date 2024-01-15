from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
import time 

#STARTS SELENIUM
service = Service(executable_path="geckodriver.exe")

options = webdriver.FirefoxOptions()
#options.add_argument("-headless")

driver = webdriver.Firefox(options=options, service=service)
driver.get('https://lacocinalatina.club/recetas/metodo/horno/')

#It closes the pop up in the "Cocina Latina" web page
close_popup = driver.find_element(By.CLASS_NAME, 'mc-closeModal').click()
#It saves the "Cocina Latina" source page
cocina_latina_source = driver.page_source

#STARTS BEAUTIFUL SOUP
soup = BeautifulSoup(cocina_latina_source, 'lxml')

#It searches for the "Cocina Latina" recipes
recipes = soup.find_all('span', class_ = 'cooked-recipe-card-content')

#A loop to extract the information of each recipe
for recipe in recipes:
    
    title = recipe.find('a').text
    
    #Checks if the title contains the word "Pan"
    if 'Pan' in title:
        
        #QUE TOME ANTES DE ESTO EL NOMBRE DEL AUTOR
        
        #It search with selenium the hyperlink with the title in the text
        #Then it runs a script to scroll down into view of the element
        #The it clicks on the element to go into the respective directory
        more_info = driver.find_element(By.PARTIAL_LINK_TEXT, title)
        driver.execute_script("arguments[0].scrollIntoView();", more_info)
        more_info.click()
        
        #BEAUTIFUL SOUP O SELENIUM PARA BUSCAR LOS INGREDIENTES Y LA DURACIÓN
        
        
        time.sleep(4)
        driver.back()
        time.sleep(3)
        
        # bread_url = driver.current_url
        # bread_page = BeautifulSoup(bread_url, 'lxml')
        
        # total_time = bread_page.find('span', class_ = 'cooked-total-time cooked-time')
        # print(total_time)
        
        
        


# driver.quit()