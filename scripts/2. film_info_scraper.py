import numpy as np
import pandas as pd
import selenium
from tqdm import tqdm
import time
import re

from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


def extract_numbers(text):
    match = re.search(r'[\d,]+', text)
    if match:
        number = match.group().replace(',', '')
        return int(number)
    return None


def get_film_info(film_name):

    webdriver_path = 'geckodriver'
    options = Options()
    options.set_preference('profile',webdriver_path)
    driver = Firefox(options = options)

    film_info = []

    #data_file = pd.read_csv("df_tv.csv")
    data_file = pd.read_csv("film_infos.csv")
    #print(data_file)
    page_urls = list(data_file["Page URL"])



    for page in tqdm(page_urls):

        try:
            driver.get(page)

            heading = driver.find_element(By.CLASS_NAME, 'c-productHero_title')
            heading_text = heading.find_element(By.TAG_NAME, 'h1').text            #Heading
            #print(heading_text)

            scores = driver.find_elements(By.CLASS_NAME, 'c-siteReviewScore')
            scores =  scores[:2] 
            metascore =  scores[0].find_element(By.TAG_NAME, 'span').text.strip() #metascore
            user_score = scores[1].find_element(By.TAG_NAME, 'span').text.strip() #user_score
            #print(f"{metascore} ================ {user_score}")


            reviewsTotal = driver.find_elements(By.CLASS_NAME, 'c-productScoreInfo_reviewsTotal')
        
            critic_number_text =  reviewsTotal[0].find_element(By.TAG_NAME, 'span').text #critic review text
            critic_number = extract_numbers(critic_number_text) #critic number

            user_number_text = reviewsTotal[1].find_element(By.TAG_NAME, 'span').text #user review text
            user_number = extract_numbers(user_number_text) #user number
            #print(f"{critic_number} ================ {user_number}")

            summary_elem = driver.find_element(By.CLASS_NAME, 'c-productDetails_description')
            summary_text = summary_elem.text  # Summary text
            #print(summary_text)


            genre_elements = driver.find_elements(By.CLASS_NAME, 'c-genreList')
            for genre in genre_elements:
                genre_string = genre.text
                #print(span.text)
            genre_list = genre_string.split('\n') #Genres
            #print(genre_list) 

            category = data_file.loc[data_file['Page URL'] == page, 'Category'].iloc[0]

            film_info.append({
                "Title": heading_text,
                "Category": category,
                "Url": page,
                "Metascore": metascore,
                "Number of critic reviewers": critic_number,
                "User score": metascore,
                "Number of user reviewers": user_number,
                "Plot summary": summary_text,
                "Genres": genre_list
            })


            df = pd.DataFrame(data=film_info, columns=film_info[0].keys())
            df.to_csv("film_details.csv", index=False)

            time.sleep(3)
            

        except:

            time.sleep(3)

        

film_info = get_film_info('film_name')
print("Done")

