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
from selenium.webdriver.support import expected_conditions as EC


def extract_numbers(text):
    match = re.search(r'[\d,]+', text)
    if match:
        number = match.group().replace(',', '')
        return int(number)
    return None

def extract_multiple_numbers_listed(text):
    # Find all numerical values using regular expressions
    number_list = [int(num) for num in re.findall(r'\d+', text)]
    return number_list


def substrings(text,start_substring,end_substring):    
    start_index = text.find(start_substring)
    end_index = text.find(end_substring)
    #print(start_index,end_index)

    start_index += len(start_substring) 
    extracted_text = text[start_index:end_index]
    #print("##############################################################")
    #print(extracted_text)
    return extracted_text


def get_film_info(film_name):

    webdriver_path = 'geckodriver'
    options = Options()
    options.set_preference('profile',webdriver_path)
    driver = Firefox(options = options)

    film_info = []

    data_file = pd.read_csv("df_tv.csv")
    #data_file = pd.read_csv("film_infos.csv")
    #print(data_file)
    page_urls = list(data_file["Page URL"])
    categories = list(data_file["Category"])



    for category, page in tqdm(zip(categories,page_urls)):

        try:
            driver.get(page)

            heading = driver.find_element(By.CLASS_NAME, 'c-productHero_title')
            heading_text = heading.find_element(By.TAG_NAME, 'h1').text            #Heading
            print(heading_text)

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

            award_elem = driver.find_elements(By.CLASS_NAME, 'c-productionAwardSummary_awards')
            
            for award_string in award_elem:
                award_string = award_string.text

            awards = []
            wins_and_noms = []
            awards_and_wins = award_string.split("\n")
            for i in awards_and_wins:
                if i[0] == "•":
                    wins_and_noms.append(i)
                else:
                    awards.append(i)

            award_titles = awards #all award titles
            total_awards = len(award_titles) #total number of award titles

            # print(awards)
            # print(wins_and_noms)

            numbers = []
            for text in wins_and_noms:
                numbers.append(extract_multiple_numbers_listed(text))

            total_wins = 0 #Total wins
            total_nomis = 0 #Total Nominations
            award_dict = {} #All awards in dictionary of strings format

            for i,j in zip(numbers, award_titles):
                award_dict[j] = f"Wins {i[0]} | Nominations: {i[1]}  \n"
                total_wins += i[0]
                total_nomis += i[1]
            
        

            #detail_infos = driver.find_elements(By.CLASS_NAME, 'c-movieDetails')
            detail_infos = driver.find_elements(By.CLASS_NAME, 'c-ProductionDetails_grid')
            
            #print(detail_infos)
            for detail in detail_infos:
                detail_string = detail.text
                #print("================")
            print(detail_string) #All details

            production_companies = substrings(detail_string,"Production Company","Release Date").strip()
            production_companies = production_companies.split(", ") # production companies
            print(production_companies)  
            production_companies_total = len(production_companies) # number of production companies
            print(production_companies_total)


            print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

            if category == 'movie':
                
                season_numbers = "N/A"
                total_epi_numbers = "N/A"
                season_release_years = "N/A"
                
                try:
                    tagline = substrings(detail_string,"Tagline","Website").strip()
                    if "\n" in tagline:
                        tagline = "N/A"
                    else:
                        pass
                except:
                    tagline = "N/A"

                #print(tagline) #Tagline


                try:
                    duration_string = substrings(detail_string,"Duration","Rating")
                    times = extract_multiple_numbers_listed(duration_string)
                    if len(times) > 1:
                        total_mins = times[0]*60 + times[1] 
                        runtime_string = f"{times[0]} Hour(s) {times[1]} Minute(s) | {total_mins} Minutes (Total)"
                    else:
                        total_mins = times[0]*60 
                        runtime_string = f"{times[0]} Hour(s) | {total_mins} Minutes (Total)"

                except:
                    runtime_string = "N/A"
                
                #print(runtime_string) #Runtime


                director_xpath = '/html/body/div[1]/div/div/div[2]/div[2]/div[1]/div/div/div[2]/div[1]/div[2]/div[2]/div[1]/p'
                directors = driver.find_elements(By.XPATH, director_xpath)
                for director in directors:
                    director_string = director.text
                
                start_index = director_string.find("Directed By: ") + len("Directed By: ")
                extracted_director_text = director_string[start_index:]

                if "," in extracted_director_text.strip():
                    directors = extracted_director_text.split(",")
                else:
                    directors = [extracted_director_text]

                print("Directors:", directors) #Director names
                
                
                
                writer_xpath   = '/html/body/div[1]/div/div/div[2]/div[2]/div[1]/div/div/div[2]/div[1]/div[2]/div[2]/div[2]/p'
                writers = driver.find_elements(By.XPATH, writer_xpath)
                for writer in writers:
                    writer_string = writer.text 

                start_index = writer_string.find("Written By: ") + len("Written By: ")
                extracted_writer_text = writer_string[start_index:]

                if "," in extracted_writer_text.strip():
                    writers = extracted_writer_text.split(",")
                else:
                    writers = [extracted_writer_text]

                print("Writers:", writers) # Writer names


            else:

                directors = "N/A"
                duration = "N/A"
                writers = "N/A"
                tagline = "N/A"

                print("================================================================================")
                print(tagline)
                print("================================================================================")

                seasons = driver.find_elements(By.CLASS_NAME, 'c-globalCarousel_fade')
                print(seasons)



            
            # film_info.append({
            #     "Title": heading_text,
            #     "Category": category,
            #     "Url": page,
            #     "Metascore": metascore,
            #     "Number of critic reviewers": critic_number,
            #     "User score": metascore,
            #     "Number of user reviewers": user_number,
            #     "Summary": summary_text,
            #     "Genres": genre_list,

            #     "Awards": award_dict,
            #     "Total titles": total_awards,
            #     "Total wins": total_wins,
            #     "Total nominations": total_nomis,


            #     "Production companies":production_companies,
            #     "Total production companies": production_companies_total,


            #     "Tagline": tagline,
            #     "Directors": directors,
            #     "Writers": writers,
            #     "Runtime": runtime_string,
            #     "Total number of seasons" : season_numbers,
            #     "Total number of episodes":total_epi_numbers,
            #     "Season release years":season_release_years,
            

            # })
            # df = pd.DataFrame(data=film_info, columns=film_info[0].keys())
            # df.to_csv("film_details.csv", index=False)
            
            # time.sleep(3)

        except:
            #time.sleep(3)
            pass

film_info = get_film_info('film_name')
print("Done")

