import json
import os
from typing import Any, Dict
from litellm import completion
from dotenv import load_dotenv

# You can replace these with other models as needed but this is the one we suggest for this lab.
MODEL = "groq/llama-3.3-70b-versatile"

load_dotenv()
api_key = os.getenv("GROK_API_KEY")

def get_itinerary(destination: str) -> Dict[str, Any]:
    """
    Returns a JSON-like dict with keys:
      - destination
      - price_range
      - ideal_visit_times
      - top_attractions
    """
    # implement litellm call here to generate a structured travel itinerary for the given destination

    # See https://docs.litellm.ai/docs/ for reference.

    prompt = f"""Generate a travel itinerary for {destination}. 

    Provide the following information in JSON format:
    - destination: The destination name
    - price_range: Expected price range for travel (use categories like 'Budget', 'Moderate', 'Expensive')
    - ideal_visit_times: List of best times to visit (seasons or specific months)
    - top_attractions: List of 3-5 must-see attractions
    
    Respond ONLY with valid JSON matching this structure.
    The response from your implemented API call should look something like what is shown below:

    {{
        "destination": "...",
        "ideal_visit_times": [
            ...
        ],
        "price_range": ...,
        "top_attractions": [
          ...
        ]
    }}
    """
    
    response = completion(
        model = MODEL,
        messages = [
            {
                "role": "system",
                "content": "You are a travel advisor that provides structured travel information in JSON format."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        api_key = api_key,
        response_format={"type": "json_object"}
      )

    content = response.choices[0].message.content
    data = json.loads(content)
    return data

if __name__ == "__main__":
  get_itinerary("Arizona")