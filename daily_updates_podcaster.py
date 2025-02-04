from crewai import Agent, Task
from crewai.tools import tool
from gtts import gTTS
from datetime import datetime
import os

@tool("Podcast Tool")
def podcast_tool(file_path: str) -> str:
    """
    Converts the text from a file into a podcast audio file.

    Args:
        file_path (str): The path to the text file to be converted.

    Returns:
        str: The path to the generated podcast audio file.
    """
    audio_file_name = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_podcast.mp3"
    audio_file_path = os.path.join("audio_files", audio_file_name)

    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    tts = gTTS(text=text, lang="en")
    tts.save(audio_file_path)
    return audio_file_path

podcast_agent = Agent(
    role="Daily Updates Podcast Creator",
    goal="Create a podcast based on the daily updates",
    backstory="You are an expert Podcast Creator who specializes in creating a podcast based on the daily updates",
    verbose=True,
)

podcast_task = Task(
    description="Create a podcast based on the contents of this file: {file_path}.",
    expected_output="An mp3 audio file of the podcast.",
    agent=podcast_agent,
    tools=[podcast_tool],
)