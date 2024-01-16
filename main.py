from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException


from bs4 import BeautifulSoup
import requests
import time 

#STARTS SELENIUM
service = Service(executable_path="geckodriver.exe")

options = webdriver.FirefoxOptions()
#options.add_argument("-headless")

driver = webdriver.Firefox(options=options, service=service)
driver.get('https://www.tasteofhome.com/recipes/basic-homemade-bread/')


#It saves the "Taste of Home" source page
taste_of_home_source = driver.page_source

# #STARTS BEAUTIFUL SOUP
soup = BeautifulSoup(taste_of_home_source, 'lxml')

recipe_title = soup.find('h1', class_ = 'recipe-title').text
recipe_total_time = soup.find('div', class_ = 'total-time').p.text
recipe_makes = soup.find('div', class_ = 'makes').p.text

all_ingredients = soup.find('ul', class_ = 'recipe-ingredients__list recipe-ingredients__collection splitColumns')
recipe_inredients = []

for ingredient in all_ingredients.find_all('li'):
    recipe_inredients.append(ingredient.text)

print(recipe_inredients)
driver.quit()

# https://www.gourmet.cl/?s=pan 