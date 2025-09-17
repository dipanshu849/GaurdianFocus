import sys 
sys.path.insert(1, "helper/")


import os
import json
import requests
from dotenv import load_dotenv
from logger import get_logger   

logger = get_logger(__name__)
load_dotenv()

api_key    = os.getenv('GOOGLE_SEARCH_API_KEY')
search_key = os.getenv('SEARCH_ENGINE_ID')

URL = "https://www.googleapis.com/customsearch/v1"

def google_search(query):
    params = {
        'key': api_key,
        'cx' : search_key,
        'q'  : query
    }

    try:
        response       = requests.get(URL, params=params)
        response.raise_for_status()
        search_results = response.json()

        snippets = [item.get('snippet', '') for item in search_results.get('items', [])[:4]]

        if not snippets:
            return "No search result found."

        return snippets

    except Exception as e:
        logger.debug("Error during Google Search: %s", e)
        return "Search failed."

