from crewai import Agent, Task
from pydantic import BaseModel, Field
from typing import List
from crewai_tools import SerperDevTool
import streamlit as st
class DailyUpdatesUrls(BaseModel):
    urls: List[str] = Field(..., description="Urls which contains latest news on AI.")


daily_updates_finder = Agent(
    role="Daily Updates Finder",
    goal="Find the Urls which contains latest news on AI.",
    backstory="You are an expert Url finder who specializes in finding the Urls which contains latest news on AI.", 
    verbose=True,
)

if st.session_state.get("use_saved_urls"):
    task_description = "return these URLs: '{custom_urls}'"
else:
    task_description = "Find the Urls which contains latest news on AI."

daily_updates_task = Task(
    description=task_description,
    expected_output="List of URLs",
    agent=daily_updates_finder,
    tools=[SerperDevTool(query="latest AI news")],
    output_pydantic=DailyUpdatesUrls
)