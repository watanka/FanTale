from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv
from langchain_community.utilities import SearchApiAPIWrapper

load_dotenv()
chat_model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash", google_api_key=os.getenv("GOOGLE_API_KEY")
)


def search(topic: str):
    search = SearchApiAPIWrapper()
    # tools = [
    #     Tool(
    #         name="intermediate_answer",
    #         func=search.run,
    #         description="useful for when you need to ask with search",
    #     )
    # ]
    return search.results(topic + "personality")
