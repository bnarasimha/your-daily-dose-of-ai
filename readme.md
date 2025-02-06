# Daily Dose of AI

A Streamlit application that creates AI-powered audio podcasts from web content and custom URLs. The application scrapes content, generates summaries, and converts them into audio format for easy consumption.

## Features

### 1. Listen to AI Doses
- Browse and play audio podcasts organized by date
- Audio player with standard playback controls
- Clear organization of content with dates and timestamps

### 2. Create New AI Dose
- **Create Today's Podcast**: Automatically generates a podcast from today's AI news and updates
- **Custom URL Management**:
  - Add URLs of your choice to include in podcasts
  - View list of saved URLs with addition dates
  - Delete URLs that are no longer needed
- **Create from Saved URLs**: Generate podcasts specifically from your saved URLs

### 3. Manage AI Doses
- View all generated podcasts with creation dates and times
- Delete unwanted podcasts and their associated report files
- Organized display with easy-to-use controls

## Configuration

The application supports multiple AI providers:

1. OpenAI (default)
   - Set `AI_PROVIDER=openai`
   - Requires `OPENAI_API_KEY`

2. Anthropic Claude
   - Set `AI_PROVIDER=anthropic`
   - Requires `ANTHROPIC_API_KEY`

You can switch providers by setting the `AI_PROVIDER` environment variable in the `.env` file.

## Installation

1. Clone the repository:

git clone https://github.com/bnarasimha/daily-dose-of-ai.git

2. Navigate to the project directory:

cd daily-dose-of-ai

3. Install required packages:

pip install -r requirements.txt

4. Set up environment variables:
Create a `.env` file in the root directory and add your API keys:

## Usage

1. Start the Streamlit application:

streamlit run main.py

2. Access the application in your web browser at `http://localhost:8501`

## Project Structure

```
├── main.py                    # Main Streamlit application
├── database.py               # SQLite database operations
├── get_daily_updates.py      # Content scraping and processing
├── daily_updates_urls_finder.py  # URL finding and management
├── audio_files/             # Directory for generated audio files
├── daily_reports/          # Directory for text reports
└── custom_urls.db          # SQLite database for custom URLs
```

## Dependencies

- Python 3.10+
- Streamlit
- SQLite3
- gTTS (Google Text-to-Speech)
- Other dependencies listed in requirements.txt

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenAI for GPT models
- Streamlit for the web framework
- Google Text-to-Speech for audio generation
