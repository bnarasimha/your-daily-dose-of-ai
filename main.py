import streamlit as st
import os
from datetime import datetime
import pandas as pd
from dotenv import load_dotenv
from daily_updates_urls_finder import daily_updates_task
from database import URLDatabase
from get_daily_updates import get_content
load_dotenv()

def get_audio_files():
    # This is a placeholder function - modify the path according to your audio files location
    audio_dir = "audio_files"
    audio_files = []
    
    if os.path.exists(audio_dir):
        for file in os.listdir(audio_dir):
            if file.endswith(('.mp3', '.wav', '.ogg')):
                file_path = os.path.join(audio_dir, file)
                # Assuming the date is part of the filename in format YYYY-MM-DD
                try:
                    date_str = file.split('_')[0]  # Modify this based on your filename format
                    date = datetime.strptime(date_str, '%Y-%m-%d').date()
                    audio_files.append({
                        'date': date,
                        'filename': file,
                        'path': file_path
                    })
                except:
                    continue
    
    return sorted(audio_files, key=lambda x: x['date'], reverse=True)

def main():
    st.title("Your Daily Dose of AI")
    
    # Initialize database
    db = URLDatabase()
    
    # Create tabs
    tab1, tab2 = st.tabs(["🎧 Listen AI Doses", "➕ Create New AI Dose"])
    
    # Tab 1: Listen to Podcasts
    with tab1:
        st.header("Listen to audio files")
        
        # Get audio files
        audio_files = get_audio_files()
        
        if not audio_files:
            st.warning("No audio files found. Please check the audio directory.")
            return
        
        # Group files by date
        df = pd.DataFrame(audio_files)
        dates = df['date'].unique()
        
        # Display audio files grouped by date
        for date in dates:
            st.subheader(date.strftime('%B %d, %Y'))
            
            # Get files for this date
            daily_files = df[df['date'] == date]
            
            # Create a container for this date's files
            with st.container():
                for _, row in daily_files.iterrows():
                    col1, col2 = st.columns([1, 4])
                    with col1:
                        st.write(f"📁 {row['filename']}")
                    with col2:
                        st.audio(row['path'])
                st.divider()
    
    # Tab 2: Add Custom URL
    with tab2:
        # Section 1: Create Today's Podcast
        st.header("Create Today's AI Dose", divider=True)
        st.write("System automatically creates podcast from today's updates searching the web. Click the button below to continue.")
        if st.button("🎙️ Create Today's AI Dose", type="primary", use_container_width=True):
            with st.spinner('Creating today\'s AI Dose...'):
                result = get_content(use_saved_urls=False)
                if result:
                    st.success("Today's AI Dose created successfully!")
                else:
                    st.error("Failed to create AI Dose")

                
        st.write("")
        st.write("")

        # Section 2: Saved URLs and Create from Saved
        st.header("Create AI Dose from Saved URLs", divider=True)
        st.write("System automatically creates podcast from saved URLs. You can add any URL to this list by entering the URL and clicking Add URL button. Finally click the 'Create Podcast from Saved URLs' below to continue.")
        # Section 3: Add Custom URL
        st.subheader("Add Custom URL")
        new_url = st.text_input(
            "Enter URL to include in podcast:", 
            placeholder="https://example.com"
        )
        
        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            if st.button("Add URL", use_container_width=True):
                if new_url:
                    if db.add_url(new_url):
                        st.rerun()
                    else:
                        st.warning("URL already exists in database")
                else:
                    st.warning("Please enter a valid URL")
        
        
        urls = db.get_all_urls()
        if urls:
            for url, added_date in urls:
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.write(url)
                with col2:
                    st.write(datetime.strptime(added_date, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d'))
                with col3:
                    if st.button("Delete", key=url):
                        if db.delete_url(url):
                            st.rerun()
            
            # Add some space before the button
            st.write("")
            
            # Create Podcast from Saved URLs button
            if st.button("📑 Create AI Dose from Saved URLs", type="primary", use_container_width=True):
                with st.spinner('Creating AI Dose from saved URLs...'):
                    result = get_content(use_saved_urls=True)
                    if result:
                        st.success("AI Dose from saved URLs created successfully!")
                    else:
                        st.error("Failed to create AI Dose")
        else:
            st.info("No custom URLs added yet")


if __name__ == "__main__":
    main()
