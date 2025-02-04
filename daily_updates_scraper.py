from crewai import Agent, Task
from crewai_tools import ScrapeWebsiteTool
from pydantic import BaseModel, Field
from typing import List

class DailyUpdates(BaseModel):
    title: str = Field(..., description="Title of the news")
    summary: str = Field(..., description="Summary of the news")
    url: str = Field(..., description="Url of the news")

class DailyUpdatesList(BaseModel):
    updates: List[DailyUpdates] = Field(..., description="List of daily updates")

daily_updates_scraper_agent = Agent(
    role="Web Scraper",
    goal="Scrape the given Urls: {urls} for latest news on AI",
    backstory="You are an expert Web Scraper who specializes in scraping the given Urls: {urls} for latest news on AI",
    verbose=True
)

daily_updates_scrape_task = Task(
    description="Scrape the given Urls: {urls} for latest news on AI",
    expected_output="include title, summary, and url of the news. Summary should be a short description of the news. can be 3 to 4 sentences.",
    agent=daily_updates_scraper_agent,
    tools=[ScrapeWebsiteTool(urls="{urls}")],
    output_pydantic=DailyUpdatesList
)

