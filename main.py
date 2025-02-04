import streamlit as st
import os
from datetime import datetime
import pandas as pd
from dotenv import load_dotenv
from daily_updates_urls_finder import daily_updates_task

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
    st.write("Listen to audio files organized by date")
    
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
        # Create a date header with formatting
        st.header(date.strftime('%B %d, %Y'))
        
        # Get files for this date
        daily_files = df[df['date'] == date]
        
        # Create a container for this date's files
        with st.container():
            for _, row in daily_files.iterrows():
                st.write(f"📁 {row['filename']}")
                st.audio(row['path'])
                st.divider()
        
        # Add some spacing between dates
        st.markdown("<br>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
