import os
from datetime import datetime
from dotenv import load_dotenv
from crewai import Crew,  Flow
from crewai.flow.flow import listen, start
from daily_updates_urls_finder import daily_updates_finder, daily_updates_task
from daily_updates_scraper import daily_updates_scraper_agent, daily_updates_scrape_task, DailyUpdates
from daily_updates_podcaster import podcast_agent, podcast_task
from crewai.tools import tool
from gtts import gTTS
from database import URLDatabase
import streamlit as st
load_dotenv()

class DailyUpdatesFlow(Flow):    
    @start()
    def find_daily_updates(self):  
        db = URLDatabase()
        custom_urls = [url[0] for url in db.get_all_urls()]  # Extract URLs from tuples
        print(custom_urls)
        daily_updates_finding_crew = Crew(
            agents=[daily_updates_finder], 
            tasks=[daily_updates_task]
        )

        daily_updates = daily_updates_finding_crew.kickoff(inputs={"custom_urls": custom_urls})
        return daily_updates 
    
    @listen(find_daily_updates)
    def scrape_daily_updates(self, daily_updates):
        daily_updates_scraping_crew = Crew(
            agents=[daily_updates_scraper_agent], 
            tasks=[daily_updates_scrape_task]
        )
            
        daily_updates_urls = ", ".join(daily_updates["urls"])

        daily_updates_list = daily_updates_scraping_crew.kickoff(inputs={"urls": daily_updates_urls})

        return daily_updates_list 

    @listen(scrape_daily_updates)
    def log_daily_updates(self, daily_updates_list):
        
        today = datetime.now()
        file_path = self.write_report_to_file(daily_updates_list, today)

        return file_path
    
    @listen(log_daily_updates)
    def convert_to_podcast(self, file_path):
        podcast_crew = Crew(
            agents=[podcast_agent], 
            tasks=[podcast_task]
        )

        daily_updates_podcast = podcast_crew.kickoff(inputs={"file_path": file_path})
        return daily_updates_podcast

    def write_report_to_file(self, daily_updates_list, today):
        """Write the daily updates report to a txt file"""

        reports_dir = "daily_reports"
        # Create reports directory if it doesn't exist
        if not os.path.exists(reports_dir):
            os.makedirs(reports_dir)

        # Create filename with date and time
        if st.session_state["use_saved_urls"]:
            filename = f"{today.strftime('%Y-%m-%d_%H-%M-%S')}_report_custom.txt"
        else:
            filename = f"{today.strftime('%Y-%m-%d_%H-%M-%S')}_report_daily.txt"

        file_path = os.path.join(reports_dir, filename)

        with open(file_path, 'a', newline='', encoding='utf-8') as file:
            for item in daily_updates_list["updates"]:
                file.write(f"{item.title}\n")
                file.write(f"{item.summary}\n")
                file.write(f"\n")
            file.write("\n")        

        return file_path


def get_content(use_saved_urls=False):
    st.session_state["use_saved_urls"] = use_saved_urls
    flow = DailyUpdatesFlow()
    result = flow.kickoff()  
    return result


if __name__ == "__main__":
    get_content()



