# standard
import json
import os
import sys 
sys.path.insert(1, "helper/")
sys.path.insert(1, "tools")
sys.path.insert(1, "actions")
import re # removing non-essential parts of response from 2nd brain
import time
from logger import get_logger   
logger = get_logger(__name__)
# installed
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai import errors as ge

# custom
import webSearch as ws
import secondBrain as sb
from notification import send_notification

load_dotenv()

MAX_RETRY = int(os.getenv('FIRST_BRAIN_MAX_RETRY'))
NOTIFICATION_TIMEOUT = int(os.getenv('NOTIFICATION_TIMEOUT_FOR_ADVICE'))

client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

def analyseData(data):
    prompt = f"""
        You are a productivity assistant. Your goal is to determine if a user's recent browser activity is productive or distracting.
        Analyze the following list of browser tabs.

        Consider the context. For example, YouTube can be for learning (tutorials, lectures) or for entertainment (music videos, gaming). Stack Overflow is almost always productive for a developer. Social media sites are usually distracting.

        Here is the user's recent activity:
        {data}

        Based on this data, use all three the title, url and identify any tabs that seem distracting or unproductive.
        Respond ONLY with a JSON object. The object should have a key "distracting_tabs", which is a list of objects. Each object in the list should have the "id [the one provided]" "title" "confidence [bw 0 and 1, how sure you are about 'distracting' or 'productive']" and a "reason" for why it's distracting. If no tabs are distracting, return an empty list.

        Example Response:
        {{
        "distracting_tabs": [
            {{
            "id": 5,
            "title": "Pythonist - YouTube",
            "reason": "This appears to be a general browsing channel, but pythonist, can be related to python, so confidence low"
            }}
        ]
        }}
    """

    response = None

    for attempt in range(1, MAX_RETRY + 1):
        try:
            response = client.models.generate_content(
            model    = os.getenv('FIRST_BRAIN_MODEL'),
            contents = prompt,
                # config   = types.GenerateContentConfig(      # disable thinking
                #     thinking_config = types.ThinkingConfig(thinking_budget=0)
                # ),
            )
            break;

        except ge.ServerError as e:
            logger.debug("Gemini overload (attempt %s): %s", attempt, e)
            if attempt == MAX_RETRY:
                logger.debug("Gemini still down - skipping this cycle.")
                return  # abort gracefully
            time.sleep(2 ** attempt)  # exponential back-off


    json_response = json.loads(response.text.strip().replace("```json", "").replace("```", "")) # DO ERROR HANDLING HERE

    moreInfo = []
    for categories in json_response:
        for dist_tab in json_response[categories]:
            # if (dist_tab["confidence"] < 0.8):
                moreInfo.append(dist_tab)

    logger.debug("First Brain response: %s", moreInfo)

    finalDecision = None
    if (len(moreInfo) != 0):
        addedInfoTabs = getMoreData(moreInfo)
        finalDecision = sb.getFinalSay(addedInfoTabs)

    if finalDecision:
        logger.debug("Final decision: %s", finalDecision)
        json_part = re.sub(r'<think>.*?</think>', '', finalDecision, flags=re.S).strip()
        json_obj  = json.loads(json_part.strip().replace("```json", "").replace("```", ""))

        print("Sub-cleaned: ",json_part)
        print("Final obj: ", json_obj)

        if json_obj["final_decision"] and json_obj["notification_message"]:
            if not json_obj["help"]:
                json_obj["help"] = ""
            title   = json_obj["final_decision"]
            message = json_obj["notification_message"] + " " + json_obj["help"]
            
        send_notification(title, message, NOTIFICATION_TIMEOUT)


    # else: #
    


def getMoreData(moreInfoArr):
    for tab in moreInfoArr:
        response = ws.google_search(tab["title"])
        tab["more_info"] = response

    return moreInfoArr
