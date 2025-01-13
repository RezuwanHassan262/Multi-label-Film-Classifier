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

In total, I scraped **15k+** movie descriptions, genres, and other relevant information about them.

<h2 style=color:#fe5e21;>Data Processing</h2>

The initial dataset contained 2186 distinct genre combinations. To streamline the analysis, I removed rare combinations occurring less than 151 times (approximately 1% of the dataset), resulting in 1807 combinations being excluded. Subsequently, null entries and duplicate rows were removed, yielding a final dataset of 15,149 samples. This cleaned and refined dataset, named film_infos.csv, is available within the data directory. The version used for model fine-tuning, film_genre_data.csv, was further processed from this dataset.

<h2 style=color:#fe5e21;>Modeling</h2>

I leveraged a pre-trained transformer model called `distilrobera-base` from HuggingFace Transformers to fine-tune it for multi-label movie genre classification. This process involved using the Fastai and Blurr libraries. The notebook containing the training code can be found [here](https://github.com/RezuwanHassan262/Multi-label-Film-Classifier/tree/main/notebooks). Feel free to explore other notebooks in the same directory for further details.



<h2 style=color:#fe5e21;>ONNX Transformation</h2>

The initial trained model had a substantial memory footprint of approximately 314MB. To optimize its size and potentially improve inference speed, I employed ONNX quantization. This technique successfully reduced the model size to a more manageable 78MB.


<h2 style=color:#fe5e21;>Deployment</h2>

<h3 style=color:#fe5e21;>HuggingFace Spaces</h3>

The compressed model, reduced to 78MB via ONNX quantization, is now deployed as a Hugging Face Spaces Gradio App. The deployment code can be found in the `deployment` folder and click [here](https://huggingface.co/spaces/Rezuwan/film_genre_classifier) to visit the HuggingFace space link 

![HF spaces screenshot](https://raw.githubusercontent.com/RezuwanHassan262/Multi-label-Film-Classifier/main/images/fgc.PNG)

<h3 style=color:#fe5e21;>Web (Flask) Deployment</h3>

Deployed a Flask web app that classifies movie genres based on their descriptions. Find the implementation in the deployment branch. Access the live app [here](somewhereonthenet).

![web deployed screenshot](https://raw.githubusercontent.com/RezuwanHassan262/Multi-label-Film-Classifier/main/images/fgcw.PNG)

Note: The image used as the background was hyperlinked from [here](Wallpapers.com/)
