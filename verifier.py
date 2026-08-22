import requests
from bs4 import BeautifulSoup
from difflib import SequenceMatcher
import re


# --------------------------------------------------
# SETTINGS
# --------------------------------------------------

THRESHOLD = 50

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0 Safari/537.36"
    )
}


# --------------------------------------------------
# CLEAN TEXT
# --------------------------------------------------

def clean_text(text):

    text = text.lower()

    text = re.sub(
        r"[^\w\s]",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# --------------------------------------------------
# SIMILARITY
# --------------------------------------------------

def calculate_similarity(input_headline, scraped_headline):

    input_clean = clean_text(input_headline)
    scraped_clean = clean_text(scraped_headline)

    input_words = set(input_clean.split())
    scraped_words = set(scraped_clean.split())

    if not input_words or not scraped_words:
        return 0

    # ----------------------------------------------
    # WORD MATCHING
    # ----------------------------------------------

    common_words = input_words.intersection(
        scraped_words
    )

    # Percentage of user's words found
    # in the original headline
    input_word_match = (
        len(common_words)
        / len(input_words)
    )

    # Percentage of original headline words
    # found in user's input
    headline_word_match = (
        len(common_words)
        / len(scraped_words)
    )

    # ----------------------------------------------
    # CHARACTER SIMILARITY
    # ----------------------------------------------

    character_score = SequenceMatcher(
        None,
        input_clean,
        scraped_clean
    ).ratio()

    # ----------------------------------------------
    # CONTAINMENT SCORE
    # ----------------------------------------------
    #
    # This is important for shortened headlines.
    #
    # Example:
    #
    # Input:
    # Karnataka IAS officer missing
    #
    # Original:
    # Karnataka IAS officer goes missing,
    # police trace his travel to Delhi
    #
    # Most important input words are present,
    # so this score becomes high.
    # ----------------------------------------------

    containment_score = input_word_match

    # ----------------------------------------------
    # FINAL SCORE
    # ----------------------------------------------

    final_score = (
        containment_score * 0.60
        +
        headline_word_match * 0.20
        +
        character_score * 0.20
    )

    return round(
        final_score * 100,
        2
    )


# --------------------------------------------------
# GET DINAMALAR HEADLINES
# --------------------------------------------------

def get_dinamalar_headlines():

    url = "https://www.dinamalar.com/"

    headlines = []

    try:

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=10
        )

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        for tag in soup.find_all("a"):

            text = tag.get_text(
                " ",
                strip=True
            )

            href = tag.get("href")

            if text and href:

                if len(text) > 20:

                    if href.startswith("/"):

                        href = (
                            "https://www.dinamalar.com"
                            + href
                        )

                    headlines.append(
                        {
                            "headline": text,
                            "url": href,
                            "source": "Dinamalar"
                        }
                    )

    except Exception as e:

        print(
            "Dinamalar error:",
            e
        )

    return headlines


# --------------------------------------------------
# GET THE HINDU HEADLINES
# --------------------------------------------------

def get_the_hindu_headlines():

    url = "https://www.thehindu.com/"

    headlines = []

    try:

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=10
        )

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        for tag in soup.find_all("a"):

            text = tag.get_text(
                " ",
                strip=True
            )

            href = tag.get("href")

            if text and href:

                if len(text) > 20:

                    if href.startswith("/"):

                        href = (
                            "https://www.thehindu.com"
                            + href
                        )

                    headlines.append(
                        {
                            "headline": text,
                            "url": href,
                            "source": "The Hindu"
                        }
                    )

    except Exception as e:

        print(
            "The Hindu error:",
            e
        )

    return headlines


# --------------------------------------------------
# GET NDTV HEADLINES
# --------------------------------------------------

def get_ndtv_headlines():

    url = "https://www.ndtv.com/"

    headlines = []

    try:

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=10
        )

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        for tag in soup.find_all("a"):

            text = tag.get_text(
                " ",
                strip=True
            )

            href = tag.get("href")

            if text and href:

                if len(text) > 20:

                    if href.startswith("/"):

                        href = (
                            "https://www.ndtv.com"
                            + href
                        )

                    headlines.append(
                        {
                            "headline": text,
                            "url": href,
                            "source": "NDTV"
                        }
                    )

    except Exception as e:

        print(
            "NDTV error:",
            e
        )

    return headlines


# --------------------------------------------------
# DETECT TAMIL
# --------------------------------------------------

def is_tamil(text):

    for char in text:

        if "\u0B80" <= char <= "\u0BFF":

            return True

    return False


# --------------------------------------------------
# VERIFY HEADLINE
# --------------------------------------------------

def verify_headline(input_headline):

    print("\nChecking headline:")
    print(input_headline)


    # ==============================================
    # TAMIL → DINAMALAR
    # ==============================================

    if is_tamil(input_headline):

        print("Language: Tamil")
        print("Checking: Dinamalar")

        articles = get_dinamalar_headlines()


    # ==============================================
    # ENGLISH → THE HINDU + NDTV
    # ==============================================

    else:

        print("Language: English")
        print("Checking: The Hindu + NDTV")

        articles = []

        articles.extend(
            get_the_hindu_headlines()
        )

        articles.extend(
            get_ndtv_headlines()
        )


    # ==============================================
    # NO ARTICLES FOUND
    # ==============================================

    if not articles:

        print(
            "No headlines found."
        )

        return {
            "verified": False,
            "similarity": 0,
            "source": None,
            "url": None
        }


    # ==============================================
    # FIND BEST MATCH
    # ==============================================

    best_score = 0
    best_article = None

    for article in articles:

        score = calculate_similarity(
            input_headline,
            article["headline"]
        )

        print(
            f"{article['source']} : "
            f"{score}% : "
            f"{article['headline'][:100]}"
        )

        if score > best_score:

            best_score = score
            best_article = article


    print(
        "\nBest similarity:",
        best_score
    )


    # ==============================================
    # 50% THRESHOLD
    # ==============================================

    if best_score >= THRESHOLD:

        print("RESULT: REAL")

        return {
            "verified": True,
            "similarity": best_score,
            "source": best_article["source"],
            "url": best_article["url"]
        }


    else:

        print("RESULT: FAKE")

        return {
            "verified": False,
            "similarity": 0,
            "source": None,
            "url": None
        }