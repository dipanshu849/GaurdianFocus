from google import genai
from google.genai import types

client = genai.Client(api_key='AIzaSyADtIkr7YsGk5nVN7d5ayPO4Ov_TwrpfAE')

def analyseData(data):
    prompt = f"""
        You are a productivity assistant. Your goal is to determine if a user's recent browser activity is productive or distracting.
        Analyze the following list of browser tabs that the user has spent a significant amount of time on.

        Consider the context. For example, YouTube can be for learning (tutorials, lectures) or for entertainment (music videos, gaming). Stack Overflow is almost always productive for a developer. Social media sites are usually distracting.

        Here is the user's recent activity:
        {data}

        Based on this data, use all three the title, url, uptime and identify any tabs that seem distracting or unproductive.
        Respond ONLY with a JSON object. The object should have a key "distracting_tabs", which is a list of objects. Each object in the list should have the "id [the one provided]" "title" and a "reason" for why it's distracting. If no tabs are distracting, return an empty list.

        Example Response:
        {{
        "distracting_tabs": [
            {{
            "id": 5,
            "title": "Pythonist - YouTube",
            "reason": "This appears to be a general browsing channel, but python ist, so its related to python"
            }}
        ]
        }}
    """

    response = client.models.generate_content(
        model    = "gemini-1.5-flash",
        contents = prompt,
        # config   = types.GenerateContentConfig(      # disable thinking
        #     thinking_config = types.ThinkingConfig(thinking_budget=0)
        # ),
    )

    print(response.text)