from flask import Flask, render_template
import requests
import json

app = Flask(__name__, template_folder=r'/home/codergamerz/Documents/My-Projects/Meme_Website_Flask/templates/')

def get_meme():
    url = "https://meme-api.com/gimme"
    response = json.loads(requests.request("GET", url).text)
    meme_large = response["preview"][-2]


@app.route('/')
def index():
    meme_pic = get_meme()
    return render_template("index.html", meme_pic=meme_pic)

app.run(host='0.0.0.0', port=5001, debug=True)
