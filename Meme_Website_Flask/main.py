from flask import Flask, render_template
from flask_ngrok import run_with_ngrok
import requests
import json

app = Flask(__name__, template_folder=r'C:\Users\shrey\OneDrive\Documents\My-Projects\Meme_Website_Flask\templates')
run_with_ngrok(app)

def get_meme():
    url = "https://meme-api.com/gimme"
    response = json.loads(requests.request("GET", url).text)
    meme_large = response["preview"][-2]
    return meme_large

@app.route('/')
def index():
    meme_pic = get_meme()
    return render_template("index.html", meme_pic=meme_pic)

app.run(host='0.0.0.0', port=5000, debug=True)
