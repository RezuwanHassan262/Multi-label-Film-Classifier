<h1 align='center' style=color:#fe5e21;><strong>Multi-label Film Classifier</strong></h1>

This classifier model can classify 27 film (Both Movie and TV Series) genres based on the provided description. <br/>
<br/>

 <h2 style=color:#fe5e21;>Data Collection</h2>

The data was scraped from the ["Rotten Tomato"](https://www.rottentomatoes.com/) website and is available [here.](https://github.com/RezuwanHassan262/Universal-Language-Model-Fine-tuning-for-Text-Classification-Implementation/blob/main/data/film_details.csv). The keys of `genre_types_encoded_multi_class.json` shows the film genre.


|             Genre             |             Genre          |            Genre           |       
|:------------------------------|:---------------------------|:---------------------------|
| 1. Action                     | 10. Thriller               | 19. Documentary            |       
| 2. Drama                      | 11. Film-Noir              | 20. Sport                  |
| 3. Crime                      | 12. Comedy                 | 21. Sci-Fi                 |
| 4. Biography                  | 13. Musical                | 22. News                   |
| 5. Adventure                  | 14. Family                 | 23. Horror                 |
| 6. War                        | 15. Animation              | 24. Game-Show              |
| 7. Mystery                    | 16. Fantasy                | 25. Talk-Show              |
| 8. History                    | 17. Western                | 26. Reality-TV             |
| 9. Romance                    | 18. Music                  | 27. Unknown                |

The scripts I've used to scrape the data can be found in the [`scrapers`](https://github.com/RezuwanHassan262/Multi-label-Film-Classifier/tree/main/scripts) directory. 

In total, I scraped **15k+** movie descriptions, genres and other relevant information about them.

