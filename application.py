from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
import requests
import json

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

db = SQL("sqlite:///wiki_read.db")


@app.route("/")
def index():

    articles = lookup()

    return render_template("index.html", articles=articles)




def lookup():
    random_url = "https://en.wikipedia.org/w/api.php?action=query&list=random&rnnamespace=0&rnlimit=10&format=json"
    article_url = "https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro=&explaintext=&pageids="
    image_url = "https://en.wikipedia.org/w/api.php?action=query&format=json&prop=images&pageids="
    response = json.loads(requests.get(random_url).text)
    response = response.get("query").get("random")

    articles = {}


    print()

    for article in response:
        text_url = f"{article_url}{article['id']}"
        image = f"{image_url}{article['id']}"

        parsed_text = json.loads(requests.get(text_url).text)
        parsed_text = parsed_text.get("query").get("pages").get(str(article["id"])).get("extract")

        parsed_image = json.loads(requests.get(image).text)
        print(parsed_image)

        articles.update( {article["id"]: [article["title"], parsed_text]} )

    return articles



# https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro=&explaintext=&pageids=11089416