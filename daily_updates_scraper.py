from crewai import Agent, Task
from crewai_tools import ScrapeWebsiteTool
from pydantic import BaseModel, Field
from typing import List
from ai_config import create_agent

class DailyUpdates(BaseModel):
    title: str = Field(..., description="Title of the news")
    summary: str = Field(..., description="Summary of the news")
    url: str = Field(..., description="Url of the news")


class DailyUpdatesList(BaseModel):
    updates: List[DailyUpdates] = Field(..., description="List of daily updates")

daily_updates_scraper_agent = create_agent(
    role="Web Scraper",
    goal="Scrape the given URLs for latest news on AI and create detailed summaries",
    backstory="You are an expert Web Scraper who specializes in extracting and summarizing AI news content.",
    verbose=True
)

daily_updates_scrape_task = Task(
    description="""
    1. Scrape each URL provided in this comma separated list: {urls}.
    2. For each URL:
       - Extract the main article title
       - Create a comprehensive 3-4 sentence summary
       - Include the source URL
    3. Format the information into a structured list of updates.
    4. Ensure each update has a title, summary, and URL.
    """,
    expected_output="""
    You must return a list of updates where each update contains:
    - title: The main headline or title of the article
    - summary: A 3-4 sentence summary of the key points
    - url: The source URL
    
    Example format:
    {
        "updates": [
            {
                "title": "Major AI Breakthrough Announced",
                "summary": "Researchers have achieved a significant milestone in AI development. The new system demonstrates unprecedented capabilities in natural language understanding. This breakthrough could revolutionize how AI systems interact with humans.",
                "url": "https://example.com/ai-news"
            },
            // ... more updates ...
        ]
    }
    """,
    agent=daily_updates_scraper_agent,
    tools=[ScrapeWebsiteTool(urls="{urls}")],
    output_pydantic=DailyUpdatesList
)
