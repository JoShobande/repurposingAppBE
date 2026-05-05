from fastapi import FastAPI
from pydantic import BaseModel
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs


ytt_api = YouTubeTranscriptApi()
app = FastAPI()

class RepurposeRequest(BaseModel):
    url: str


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


def extractionLogic(youtubeUrl:str):
    video_id = get_youtube_id(youtubeUrl)
    result = ytt_api.fetch(video_id) 
    try:
        for snippets in result:
            
            return (snippets.text)
    except:
        print("Something went wrong")
    




@app.get("/")
def root():
    return {"Hello": "World"}


@app.post("/repurpose/")
async def repurpose_content(data: RepurposeRequest):
    if "youtube" in data.url:
        return 'youtube'
    else:
        return 'blog'
    


extractionLogic('https://www.youtube.com/watch?v=F4rN2OaMdcs')
