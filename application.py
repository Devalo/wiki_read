from flask import Flask, render_template, request
import requests
import json

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True



@app.route("/", methods=["GET", "POST"])
def index():
    number = 10

    if request.method == "POST":
        number = request.form.get("amount")
        if number == "":
            number = 10

        articles = lookup(number)

        return render_template("index.html", articles=articles)

    else:
        articles = lookup()
        return render_template("index.html", articles=articles)




def lookup(amount = 10):
    # Set up urls to hit wikipedia API
    random_url = f"https://en.wikipedia.org/w/api.php?action=query&list=random&rnnamespace=0&rnlimit={amount}&format=json"
    article_url = "https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro=&explaintext=&pageids="
    image_url = "https://en.wikipedia.org/w/api.php?action=query&format=json&prop=images&pageids="

    # Create main api call
    response = json.loads(requests.get(random_url).text)
    response = response.get("query").get("random")

    # Dictionary to build the pack served to the tempate
    articles = {}



    for article in response:
        # Urls to get main text and image from API
        text_url = f"{article_url}{article['id']}"
        image = f"{image_url}{article['id']}"

        # Parse json to collect pure text
        parsed_text = json.loads(requests.get(text_url).text)
        parsed_text = parsed_text.get("query").get("pages").get(str(article["id"])).get("extract")


        #Collect image
        # Build article with image, title, text
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

