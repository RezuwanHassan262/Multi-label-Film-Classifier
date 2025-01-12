import gradio as gr
import onnxruntime as rt
from transformers import AutoTokenizer
import torch, json

tokenizer = AutoTokenizer.from_pretrained("distilroberta-base")

with open("genre_types_encoded_multi_class.json", "r") as fp:
  encode_genre_types = json.load(fp)

genres = list(encode_genre_types.keys())


inf_session = rt.InferenceSession('film_genre_classifier_quantized.onnx')
input_name = inf_session.get_inputs()[0].name
output_name = inf_session.get_outputs()[0].name


def classify_film_genre(description):
  input_ids = tokenizer(description)['input_ids'][:512]
  logits = inf_session.run([output_name], {input_name: [input_ids]})[0]
  logits = torch.FloatTensor(logits)
  probs = torch.sigmoid(logits)[0]
  return dict(zip(genres, map(float, probs))) 

label = gr.Label(num_top_classes=5)
iface = gr.Interface(fn=classify_film_genre, 
                     inputs="text", 
                     outputs=label,
                     title="Film Genre Classifer",
                     description=(
        f"""
        
        Instructions:
        
        1. Copy and paste a movie plot from the internet.
        2. Hit the Submit button.
        
        Note: There are a total of 27 Genres to classify

        
        """
    )
                    )
iface.launch(inline=False)
