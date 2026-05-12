from fastapi import FastAPI
from pydantic import BaseModel
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
import requests
from bs4 import BeautifulSoup
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

ytt_api = YouTubeTranscriptApi()
app = FastAPI()

class RepurposeRequest(BaseModel):
    url: str
    platform: str

client = anthropic.Anthropic(
    api_key=os.getenv("ANTHROPIC_KEY")
)

def get_youtube_id(url):
    parsed = urlparse(url)
    # case 1: youtube.com/watch?v=...
    if "youtube.com" in parsed.netloc:
        query = parse_qs(parsed.query)
        return query.get("v", [None])[0]

    # case 2: youtu.be/...
    if "youtu.be" in parsed.netloc:
        return parsed.path.lstrip("/")

    return None


def youtube_extraction(youtube_url:str):
    
    video_id = get_youtube_id(youtube_url)

    try:
        result = ytt_api.fetch(video_id) 
        whole_text = ""
        for snippets in result:
            whole_text += snippets.text
        return whole_text
    except:
        return "No transcript available for this video"
   


def blog_extraction(blog_url:str):
    whole_text = ""
    try:
        html_data = requests.get(blog_url)
        parser_result = BeautifulSoup(html_data.content, "html.parser")
        for tags in parser_result.find_all(['h1','h2', 'h3', 'p',]):
            whole_text+= tags.text
        return whole_text
    except:
        return 'an error occured. try again'
    
     

def generate_content(extracted_text:str, platform:str):
    prompt = (
        f"come up with an engaging content for {platform} using the context discussed in the following text. "
        f"repurpose it to fit {platform}'s audience. make it very interesting and engaging. "
        f"Let the number of characters be less or equal to the maximum number of characters allowed in the {platform} (if any limit) per thread. "
        f"if repurposing for twitter or thread, Come up with not more than 4 tweets or threads for the entire thread. "
        f"The generated content should include key words surrounding the context that will grab peoples attention. "
        f"the hook should also be eye catching. "
        f"Return the response in a json format separating each tweet if repurposing for twitter or thread."
        f"Below is the extracted text:" +
        extracted_text
    )
    try:
        message = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1000,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )
        return message.content
    except Exception as e:
        return str(e)


@app.get("/")
def root():
    return {"Hello": "World"}
    

@app.post("/repurpose/")
async def repurpose_content(data: RepurposeRequest):
    if "youtube" in data.url:
       result = youtube_extraction(data.url)
    else:
        result = blog_extraction(data.url)
    return generate_content(result, data.platform)
        
    

    




