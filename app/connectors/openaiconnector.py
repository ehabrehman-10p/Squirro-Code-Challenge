from typing import List
from fastapi import HTTPException
from openai import OpenAI
from config import config

openai_key = config.OPENAI_API_KEY
if openai_key is None:
    raise ValueError("OpenAI API key not found in the env file.")

client = OpenAI(api_key=openai_key)



def generate_response(query: str, documents: List[str]):
    try:
        prompt = f"""Consider yourself a search engine.Please provide an answer to {query} based on the information contained within the following documents: {', '.join(documents)}.
        Your response should be derived solely from the content of these documents, without introducing external information."""
        response = client.chat.completions.create(
            model = "gpt-3.5-turbo-16k",
            messages = [{"role" : "system", "content" : [{"type" : "text" , "text" : prompt}]}],
            max_tokens = 1500,
            temperature = 0.2,
            top_p = 1.0,
            n=1,
            stop="\n"  )

        if response.choices[0]:
            generated_response = response.choices[0].message.content.strip()
            return  generated_response
        return f"Error: OpenAI API response did not contain valid data"

    except Exception as e:
      raise HTTPException(500, "Internal Server Error.")
