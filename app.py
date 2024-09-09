import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()

from youtube_transcript_api import YouTubeTranscriptApi
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

prompt="""You are a Youtube video summarizer. you will be taking transcript text as input and you have to summarize the entir video, and give important 
summary in points within 250 words limit. Please provide the summary of the text given here : """

def get_transcript(url):
  try:
    video_id=url.split("=")[1]
    transcript_text = YouTubeTranscriptApi.get_transcript(video_id)
    transcript=""
    for i in transcript_text:
      transcript+=" "+i['text']
    return transcript
  except Exception as e:
    raise e

  
def generate_gemini(transcript_text,prompt):
  model = genai.GenerativeModel("gemini-1.5-flash")
  response = model.generate_content(prompt+transcript_text)
  return response.text


st.title("Here is your YouTube summarizer")
youtube_link=st.text_input("Enter Youtube video link")

if youtube_link:
  video_id=youtube_link.split("=")[1]
  st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

if st.button("Get Summary"):
  transcript_text=get_transcript(youtube_link)
  if transcript_text:
    summary=generate_gemini(transcript_text,prompt)
    st.markdown("Here is the summary")
    st.write(summary)

