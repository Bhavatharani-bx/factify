from flask import Flask, render_template, request
from realtime.verifier import verify_headline

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():

    prediction = None
    confidence = None
    source = None
    article_url = None

    if request.method == "POST":

        news = request.form.get("news")

        if news and news.strip():

            news = news.strip()

            result = verify_headline(news)

            if result["verified"]:

                prediction = "Real"
                confidence = result["similarity"]
                source = result["source"]
                article_url = result["url"]

            else:

                prediction = "Fake"

                confidence = None
                source = None
                article_url = None

    return render_template(
        "index.html",
        prediction=prediction,
        confidence=confidence,
        source=source,
        article_url=article_url
    )


if __name__ == "__main__":
    app.run(debug=True)