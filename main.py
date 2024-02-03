from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import time 
import pandas as pd
import random

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

#STARTS BEAUTIFUL SOUP
#For loop to repeat the actions based on the amount of recipes
counter = 1
while True:
    
    try:
    
        #Start page with all the recipes buttons
        driver.get('https://www.tasteofhome.com/collection/recipes-for-homemade-bread/')

        #Check if the recipe button exists and then click it
        wait = WebDriverWait(driver, 5)
        bread = wait.until(EC.presence_of_element_located((By.XPATH, ('(//div[@class="listicle-page__cta-button"])['+ str(counter) + ']'))))
        bread.click()

        #Gets the recipe URL and then use it as the source for beautiful soup to search the info
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

        print(counter+") "+recipe_title)
        
        #Add to the counter 
        counter+=1

        driver.back()
        time.sleep(random.randint(1, 5))
    
    except TimeoutException:
        #If the 5 second wait to find the button passes, it means that the button doesn't exist and it breaks the loop
        break
    
    except Exception as error:
        print("An exception occurred:", type(error).__name__)
    
# #Create data frame with the dictionary and uses it to create a csv file with the data 
df = pd.DataFrame(data)
df.to_csv('scraped_data.csv', index=False)

driver.quit()
