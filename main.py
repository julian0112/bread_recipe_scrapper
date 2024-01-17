from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import time 
import pandas as pd

#STARTS SELENIUM
service = Service(executable_path="geckodriver.exe")

#Selenium options for the browser
options = webdriver.FirefoxOptions()
options.add_argument("-headless")

driver = webdriver.Firefox(options=options, service=service)

#Dictionary to store data and use it to create a data frame and cvs file with pandas
data = {
    'titles': [],
    'times': [],
    'makes': [],
    'ingredients': [],
    'links': []
}


# #STARTS BEAUTIFUL SOUP

#For loop to repeat the actions an x number of times, might be change so it ends when reaches the last recipe
for x in range(3):
    
    if x == 0:
        driver.get('https://www.tasteofhome.com/recipes/basic-homemade-bread/')
        
    else: 
        driver.get(driver.current_url)

    taste_of_home_source = driver.page_source

    soup = BeautifulSoup(taste_of_home_source, 'lxml')
    
    #Gets the title, total time, amount make, ingredients and link of the recipe
    recipe_title = soup.find('h1', class_ = 'recipe-title').text
    recipe_total_time = soup.find('div', class_ = 'total-time').p.text
    recipe_makes = soup.find('div', class_ = 'makes').p.text

    all_ingredients = soup.find('ul', class_ = 'recipe-ingredients__list recipe-ingredients__collection splitColumns')
    recipe_ingredients = []

    for ingredient in all_ingredients.find_all('li'):
        recipe_ingredients.append(ingredient.text)
        
    recipe_link = driver.current_url
    
    #It adds recipe to data dictionary
    data['titles'].append(recipe_title)
    data['times'].append(recipe_total_time)
    data['makes'].append(recipe_makes)
    data['ingredients'].append(recipe_ingredients)
    data['links'].append(recipe_link)

    print(recipe_title)

    #Selenium presses the next recipe button
    try:
        driver.find_element(By.CLASS_NAME, 'next-recipe-link').click()
        
    except NoSuchElementException:
        print('Llego al final')
        
    else: 
        print('Siguiente ->')

    time.sleep(3)
    
    
#Create data frame with the dictionary and uses it to create a csv file with the data 
df = pd.DataFrame(data)
df.to_csv('scraped_data.csv', index=False)

driver.quit()
