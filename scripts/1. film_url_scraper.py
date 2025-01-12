import pandas as pd
import selenium
from tqdm import tqdm
import time

from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

film_infos = []


def after_numerics_and_dot(text):
    # Find the index of the first dot
    dot_index = text.find('.')
    
    if dot_index != -1:
        # Slice the string after the first dot and strip any leading whitespace
        x = text[dot_index:].strip()
        return x

    else:
        return ""



def get_film_names(category,page):

    # initializing the driver and firefox profile
    webdriver_path = "geckodriver"
    options = Options()
    options.set_preference('profile', webdriver_path)
    driver = Firefox(options = options)
    cat_url = f"https://www.metacritic.com/browse/{category}/"

    

    for ids in tqdm(range(1,page,1)):
        page_num = ids
        page_url = f"{cat_url}?releaseYearMin=1910&releaseYearMax=2024&page={ids}"
        driver.get(page_url)
        time.sleep(3)
        rows = driver.find_elements(By.CLASS_NAME, "c-finderProductCard")

        try:
            for row in rows:

                #print(rows) 
                url_tag = row.find_element(By.CLASS_NAME, "c-finderProductCard_title" )
                text = url_tag.text
                film_title = after_numerics_and_dot(text) # film title
                
                if rows.index(row) == 0:
                    film_title = film_title[1:]                
                else:
                    film_title = film_title[2:]

                #print(film_title)

                release_info = row.find_element(By.CLASS_NAME, "c-finderProductCard_meta")
                release_info = release_info.text.split("  •  Rated ")
                
                if len(release_info) == 2:

                    date = release_info[0] # film release date
                    rate = release_info[1] # film ratings
                
                else:
                    date = release_info[0] # film release date
                    rate = "N/A" # film ratings
                
                #print(f"{date} | {rate}")

                metascore_elem = row.find_element(By.CSS_SELECTOR, 'span[data-v-38f51ed3]')
                metascore = metascore_elem.text # film metascore

                # print(metascore)

                film_href = row.find_element(By.CLASS_NAME, "c-finderProductCard_container")
                # print(film_href)

                film_url = film_href.get_attribute("href") # film url
                # print(film_url)

                film_infos.append({
                    "Title": film_title,
                    "Category": category,
                    "Release date": date,
                    "Ratings": rate,
                    "Metascore": metascore,
                    "Page URL": film_url,

                })

            # print("=====================================================================")
            time.sleep(10)
            df = pd.DataFrame(data=film_infos, columns=film_infos[0].keys())
            df.to_csv("film_info.csv", index = False)  

        except:
            pass


    driver.close()

####################################################################################################################################################

page_info = {
    "movie":677,
    "tv": 129
    }


for category, page in page_info.items():
    category_links = get_film_names(category, page)

print("===================================")
print()
print(" =================================== All Done =================================== ")
print()
print("===================================")