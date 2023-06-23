# Web-Scrapping

## YouTube Scrapper

### Data Retrieval
- Using [YouTube API](https://developers.google.com/youtube/v3) key provided by Google to extract data for [GoogleDevelopers]((https://www.youtube.com/@GoogleDevelopers)) YouTube channel. The code is in [retrieve_all_yt_vid_data.py](https://github.com/rukshar69/Web-Scrapping/blob/main/YoutubeScrapper/retrieve_all_yt_vid_data.py)
- Extracted data includes channel subscriber, total video, total views count (stored in [channel_stats.csv](https://github.com/rukshar69/Web-Scrapping/blob/main/YoutubeScrapper/data/channel_stats.csv)) and the individual video's id, views, likes, comments, and upload date (stored in [google_dev_channel_vid_details.csv](https://github.com/rukshar69/Web-Scrapping/blob/main/YoutubeScrapper/data/google_dev_channel_vid_details.csv)).
- **Data cleaning** is performed on *views* column in [google_dev_channel_vid_details.csv](https://github.com/rukshar69/Web-Scrapping/blob/main/YoutubeScrapper/data/google_dev_channel_vid_details.csv) because some values are corrupt. So we have to drop those rows and store the cleaned data in [google_dev_vid_details_cleaned.csv](https://github.com/rukshar69/Web-Scrapping/blob/main/YoutubeScrapper/data/google_dev_vid_details_cleaned.csv)

### Streamlit App
[YouTube API Scrapped Streamlit App](https://yt-api-6zp16ra8uc.streamlit.app/)

The app includes:
- Basic info about the channel
- Scrollable table to sort out channel videos by views/likes/upload date
- Distribution/box plots for video likes/views
- Scatter plot between views and likes along with their regression
- Views/Likes by year
- Time Series Plot for Videos vs Upload Date