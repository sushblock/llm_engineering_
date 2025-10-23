import os
import logging
from dotenv import load_dotenv
from openai import OpenAI

# load environment variables
load_dotenv()

# Setting up logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO").upper(),
    format="%(asctime)s - %(levelname)s - %(message)s"
)

OPEN_MODEL=os.getenv("OLLAMA_GPT_MODEL")

# call a function to get the required llm using OpenAI decorator pattern
async def get_llm_client(llm_name: str, llm_provider: str):
    if llm_provider == "ollama":
        if llm_name == OPEN_MODEL:
            client = OpenAI(base_url=os.getenv("OLLAMA_BASE_URL"), api_key=os.getenv("OLLAMA_API_KEY"))
        else:
            client = OpenAI()
    else:
        client = OpenAI()

    return client

#get the response message from the llm
async def get_chat_response(prompt_messages, client, llm_model, temp: float):
    print("Getting LLM response")
    response = client.chat.completions.create(
        model=llm_model, messages=prompt_messages, temperature=temp
    )
    print("Got LLM response")

    return response.choices[0].message.content
