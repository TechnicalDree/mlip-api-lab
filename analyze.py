import json
import os
from typing import Any, Dict
import litellm
from litellm import completion
from dotenv import load_dotenv
from pydantic import BaseModel

# You can replace these with other models as needed but this is the one we suggest for this lab.
MODEL = "groq/llama-3.3-70b-versatile"

load_dotenv()
api_key = os.getenv("GROK_API_KEY")
litellm.enable_json_schema_validation=True

class Itinerary(BaseModel):
  destination: str
  ideal_visit_times: list[str]
  price_range: str
  top_attractions: list[str]

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
    - ideal_visit_times: List of best times to visit (seasons or specific months)
    - price_range: Expected price range for travel (use categories like 'Budget', 'Moderate', 'Expensive')
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
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "itinerary_response",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "destination": {
                            "type": "string",
                            "description": "The destination name"
                        },
                        "ideal_visit_times": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                            "description": "Best times to visit (seasons or specific months)"
                        },
                        "price_range": {
                            "type": "string",
                            "description": "Expected price range (Budget, Moderate, or Expensive)"
                        },
                        "top_attractions": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                            "description": "List of 3-5 must-see attractions"
                        }
                    },
                    "required": ["destination", "ideal_visit_times", "price_range", "top_attractions"],
                    "additionalProperties": False
                }
            }
        }
      )

    content = response.choices[0].message.content
    # data = json.loads(content)
    # return data
    itinerary = Itinerary.model_validate_json(content)
    return itinerary.model_dump()

if __name__ == "__main__":
  get_itinerary("Arizona")