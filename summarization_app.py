# imports
import os
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from rich.markdown import Markdown
from openai import OpenAI
import openai
from rich.console import Console

load_dotenv()  # Load variables from .env file

api_key = os.getenv("OPENAI_API_KEY")

# A class to represent a Webpage

class Website:
    url: str
    title: str
    text: str

    def __init__(self, url):
        self.url = url
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.title = soup.title.string if soup.title else "No title found"
        for irrelevant in soup.body(["script", "style", "img", "input"]):
            irrelevant.decompose()
        self.text = soup.body.get_text(separator="\n", strip=True)



ed = Website("https://www.rbc.com/our-company/")
# print(ed.title)
# print(ed.text)

system_prompt = "You are an assistant that analyzes the contents of a website \
and provides a short summary, ignoring text that might be navigation related. \
Respond in markdown."

def user_prompt_for(website):
    user_prompt = f"You are looking at a website titled {website.title}"
    user_prompt += "The contents of this website is as follows; \
    please provide a short summary of this website in markdown. \
    If it includes news or announcements, then summarize these too.\n\n"
    user_prompt += website.text
    return user_prompt

# pass in the prompts we just wrote
def messages_for(website):
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt_for(website)}
    ]

def summarize(url):
    # use Website class, return website body text
    website = Website(url)
    # openai api
    response = openai.chat.completions.create(
        model = "gpt-4o-mini",
        messages = messages_for(website)
    )
    return response.choices[0].message.content

#summarize("https://www.rbc.com/our-company/")

console = Console()

# uses IPython.display.Markdown to format and display the summary in Markdown
def display_summary(url):
    summary = summarize(url)
    console.print(Markdown(summary))


display_summary("https://www.rbc.com/our-company/")
