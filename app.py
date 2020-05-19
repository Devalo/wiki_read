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



    for article in response:
        text_url = f"{article_url}{article['id']}"
        image = f"{image_url}{article['id']}"

        parsed_text = json.loads(requests.get(text_url).text)
        parsed_text = parsed_text.get("query").get("pages").get(str(article["id"])).get("extract")

        parsed_image = json.loads(requests.get(image).text)

        if parsed_image.get("query").get("pages").get(str(article['id'])).get("images") != None:
            if "File" and "jpg" or "png" in parsed_image.get("query").get("pages").get(str(article['id'])).get("images")[0].get("title"):
                filename = parsed_image.get("query").get("pages").get(str(article['id'])).get("images")[0].get("title")
                filename = filename.strip("File:").replace(" ", "_")
                final_url = f"https://commons.wikimedia.org/wiki/Special:FilePath/{filename}?width=200"
                articles.update( {article["id"]: [article["title"], parsed_text, final_url]} )
            else:
                articles.update( {article["id"]: [article["title"], parsed_text]} )

        
    return articles


# https://commons.wikimedia.org/wiki/Special:FilePath/Ad-tech_London_2010_(2).JPG?width=200 
# https://commons.wikimedia.org/wiki/Special:FilePath/Wiki_letter_w.svg?width=200 

# https://commons.wikimedia.org/wiki/Special:FilePath/Ad-tech_London_2010_(2).JPG
# https://commons.wikimedia.org/wiki/Special:FilePath/Flag-map_of_Nebraska.svg