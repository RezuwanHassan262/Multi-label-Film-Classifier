from gradio_client import Client

client = Client("Rezuwan/film_genre_classifier")
result = client.predict(
		description="Hello!!",
		api_name="/predict"
)

for conf in result['confidences']:
    if conf['confidence'] >= 0.3:
        print(conf['label'])