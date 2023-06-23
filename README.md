# Web-Scrapping

## YouTube Scrapper

### Data Retrieval
- Use YouTube API key provided by Google to extract data for [GoogleDevelopers]((https://www.youtube.com/@GoogleDevelopers)) YouTube channel. The code is in [retrieve_all_yt_vid_data.py](https://github.com/rukshar69/Web-Scrapping/blob/main/YoutubeScrapper/retrieve_all_yt_vid_data.py)
- Extracted data includes channel subscriber, total video, total views count (stored in [channel_stats.csv](https://github.com/rukshar69/Web-Scrapping/blob/main/YoutubeScrapper/data/channel_stats.csv)) and the individual video's id, views, likes, comments, and upload date (stored in [google_dev_channel_vid_details.csv](https://github.com/rukshar69/Web-Scrapping/blob/main/YoutubeScrapper/data/google_dev_channel_vid_details.csv)).
- **Data cleaning** is performed on *views* column in [google_dev_channel_vid_details.csv](https://github.com/rukshar69/Web-Scrapping/blob/main/YoutubeScrapper/data/google_dev_channel_vid_details.csv) because some values are corrupt. So we have to drop those rows and store the cleaned data in [google_dev_vid_details_cleaned.csv](https://github.com/rukshar69/Web-Scrapping/blob/main/YoutubeScrapper/data/google_dev_vid_details_cleaned.csv)

### Streamlit App
