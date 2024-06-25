import json
from openai import OpenAI
from pydantic import BaseModel
from ..config import settings

client = OpenAI(api_key=settings.openai_api_key)

class MatchResult(BaseModel):
    score: float
    in_common: str
    not_in_common: str

def calculate_match_score(input1: str, input2: str) -> MatchResult:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system", 
                "content": 
                    '''
                    You are an AI that compares two profiles, one for a mentee and another for a mentor. 
                    You need to determine how well the two profiles match and whether the mentee will benefit from being matched with the mentor.
                    Do not focus on the mentor's qualifications, but rather on the compatibility between the two profiles.

                    The json object should have the following keys:
                    - score: a float representing the match score between 0.0 and 1.0
                    - in_common: a string representing the things in common and an explanation of why the people would be a good match
                    - not_in_common: a string representing the things not in common and an explanation of why the people would not be a good match

                    If the two inputs have nothing in common, set the match score to 0.0 and state that there is nothing in common.
                    If the two inputs are exactly the same, set the match score to 1.0 and state that they are exactly the same.
                    If the two inputs are similar, set the match score to a value between 0.0 and 1.0 and state what is in common and what is not in common.
                    '''    
            },
            {"role": "user", "content": f"Compare these two texts:\n\nText 1: {input1}\n\nText 2: {input2}"}
        ],
        max_tokens=500,
        response_format={"type": "json_object"}
    )
    
    with open('response.json', 'w') as f:
        f.write(response.model_dump_json())

    response_content = json.loads(response.choices[0].message.content.strip())


    return MatchResult(**response_content)