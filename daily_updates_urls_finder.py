from crewai import Agent, Task
from pydantic import BaseModel, Field
from typing import List
from crewai_tools import SerperDevTool

class DailyUpdatesUrls(BaseModel):
    urls: List[str] = Field(..., description="Urls which contains latest news on AI.")


daily_updates_finder = Agent(
    role="Daily Updates Finder",
    goal="Find the Urls which contains latest news on AI.",
    backstory="You are an expert Url finder who specializes in finding the Urls which contains latest news on AI.", 
    verbose=True,
)

daily_updates_task = Task(
    description="Find the Urls which contains latest news on AI. Once you found the urls, add these custom urls: '{custom_urls}' selected by user to the list you prepared.",
    expected_output="Urls which contains latest news on AI.",
    agent=daily_updates_finder,
    tools=[SerperDevTool(query="latest AI news")],
    output_pydantic=DailyUpdatesUrls
)