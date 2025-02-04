import streamlit as st
import os
from datetime import datetime
import pandas as pd
from dotenv import load_dotenv
from daily_updates_urls_finder import daily_updates_task
from database import URLDatabase

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
    tab1, tab2 = st.tabs(["🎧 Listen Podcasts", "➕ Add Custom URL"])
    
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
        st.header("Add Custom URL")
        new_url = st.text_input(
            "Enter URL to include in podcast:", 
            placeholder="https://example.com"
        )
        
        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            if st.button("Add URL", use_container_width=True):
                if new_url:
                    if db.add_url(new_url):
                        #st.success(f"URL added successfully: {new_url}")
                        st.rerun()
                    else:
                        st.warning("URL already exists in database")
                else:
                    st.warning("Please enter a valid URL")
        
        # Display existing URLs
        st.subheader("Saved URLs")
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
        else:
            st.info("No custom URLs added yet")

if __name__ == "__main__":
    main()
