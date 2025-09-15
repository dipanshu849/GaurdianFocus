from dotenv import load_dotenv
from groq import Groq
from groq import GroqError
import os
import sys 
sys.path.insert(1, "helper/")

load_dotenv()

from logger import get_logger   
logger = get_logger(__name__)

client = Groq(
    api_key = os.getenv("GROQ_API_KEY")
)

def getFinalSay(data):    # Error handling left
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": (f"""
                  You are a senior productivity strategist.
                  Your job is to review an initial analysis of a user's browser activity and provide a final, actionable judgment.
                  An initial analysis has assigned a tabs be potentially distracting by a confidence number (between 0 an 1).
                  Your task is to review all the tabs data and the analysis along with supplementary information and make a more nuanced decision.
                  The user's goal is not just to learn, but to be productive and efficient.
                  
                  Each will contain
                  **Initial Analysis:**
                  - Tab Title: 
                  - Tab URL: 
                  - Analyst's Reason:
                  - Supplementary Information (from a web search, which may also be irrelevent):

                  **Your Task:**
                  Critically evaluate the situation. 
                  Is the Analyst's reason valid? 
                  Even if the topic is for learning, is the user's *method* (e.g., endlessly searching YouTube) inefficient? 
                  Could they be using a better resource like official documentation or Stack Overflow?

                  For review all the tabs [all inactive and 1 active].
                  These are the tabs where user has spent more then 10 minutes.
                  These tabs may be related or can be different
                  If user can be distracted from the task user was doing.
                  Or doing that task in wrong or less-productive.
                  Or maybe user is doing some work, also opens youtube inbetween for entertainment.

                  Here is the user's recent activity:
                  {data}

                  Respond ONLY with a JSON object with two keys:
                  1. "final_decision": Should be "productive" or "distracting".
                  2. "notification_message": A helpful, encouraging message for the user explaining your reasoning. If productive, the message can be positive reinforcement [NOTE: KEEP CONCISE].
                  3. "help": A helpful resource for the user, a resource that can help user to solve their problem or a resource which can help them in their work [eg, unhook extension for youtube]

                  Example for a distracting YouTube search:
                  {{
                  "final_decision": "distracting",
                  "notification_message": "It looks like you're searching for Flask tutorials on YouTube. While learning is great, targeted searches on Stack Overflow or reading the official Flask documentation might get you answers faster."
                  "help": "If you wish to continue please install unhook web extension to don't loose focus"
                  }}
                  """
                ),
            }
        ],
        model=os.getenv('SECOND_BRAIN_MODEL'),
        temperature=float(os.getenv('SECOND_BRAIN_TEMPERATURE')),          # keep it deterministic
        max_tokens=int(os.getenv('SECOND_BRAIN_MAX_OUTPUT_TOKEN')),
    )
    # print("TOKENS used: ", chat_completion)
    # print("*******************************")
    return chat_completion.choices[0].message.content



## REF: https://console.groq.com/docs/quickstart
