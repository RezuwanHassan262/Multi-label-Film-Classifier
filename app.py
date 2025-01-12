from flask import Flask, render_template, request
from gradio_client import Client


app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    input_text = ""
    

    if request.method == 'POST':
        input_text = request.form.get('input_text', '')
        print(input_text)    
        output = predict_genres(input_text)
        confidence_list = output['confidences']
        genres = [conf['label'] for conf in confidence_list if conf['confidence'] >= 0.3]
        genre_to_show = ""

        genre_to_show = ", ".join(genres)

        print(genre_to_show)
        return render_template("index.html", input_text=input_text, output_text=genre_to_show)
    else:
        return render_template("index.html")

def predict_genres(input_text):
    client = Client("Rezuwan/film_genre_classifier")
    result = client.predict(
            description=f"{input_text}",
            api_name="/predict"
    )

    return result

if __name__ == "__main__":
    app.run(debug=True)