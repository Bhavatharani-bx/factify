# Factify - Intelligent Fake News Detection System

Factify is a bilingual fake news verification system that supports English and Tamil news headlines.

## Features

- Verifies news headlines as Real or Fake
- Supports English and Tamil
- Performs real-time headline verification
- Checks trusted news sources
- Shows the matched news article and source URL when available

## Technologies Used

- Python
- Flask
- HTML
- CSS
- JavaScript
- Bootstrap
- NLP
- BeautifulSoup
- TF-IDF
- Logistic Regression

## Trusted News Sources

- The Hindu
- Dinamalar

## How It Works

1. User enters a news headline.
2. The system identifies the language.
3. The headline is processed.
4. Factify checks trusted news websites.
5. The entered headline is compared with available headlines.
6. The system displays the verification result.

## Project Structure

- `app.py` - Flask application
- `verifier.py` - Real-time headline verification
- `index.html` - Frontend page
- `style.css` - Website styling
- `requirements.txt` - Required Python packages
- `.gitignore` - Files excluded from GitHub

## How to Run

Install the required packages:

```bash
pip install -r requirements.txt
