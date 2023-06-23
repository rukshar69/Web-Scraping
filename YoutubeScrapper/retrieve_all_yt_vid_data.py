from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv
import os
import pandas as pd
import numpy as np
load_dotenv()

def get_channel_stats(youtube, username):
    # Get channel details
    channels_response = youtube.channels().list(
        part=[
            'contentDetails',
            'contentOwnerDetails',
            'id',
            'localizations',
            'snippet',
            'statistics',
            'status',
            'topicDetails'],
        forUsername=username
    ).execute()
    return channels_response

def get_all_video_data(username, api_key):
    try:
        youtube = build('youtube', 'v3', developerKey=api_key)

        # Get channel details
        channels_response = get_channel_stats(youtube, username)
        #print(channels_response)
        if len(channels_response['items']) == 0:
            print("Channel not found.")
            return

        channel_id = channels_response['items'][0]['id']
        channel_stats = channels_response['items'][0]['statistics']
        columns = ['viewCount','subscriberCount',  'videoCount']
        values = [[channel_stats['viewCount'],channel_stats['subscriberCount'],channel_stats['videoCount']]]
        channel_stats_df = pd.DataFrame(values, columns=columns)
        # print(channel_stats_df)
        channel_stats_df.to_csv('channel_stats.csv', index=False)

        #Get uploaded videos for the channel
        uploads_playlist = channels_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

        next_page_token = None
        all_videos = []

        page = 1
        while True:
            
            playlist_items_response = youtube.playlistItems().list(
                part='contentDetails',
                playlistId=uploads_playlist,
                maxResults=50,  # Increase or decrease the number of results as needed
                pageToken=next_page_token
            ).execute()

            video_ids = []
            for item in playlist_items_response['items']:
                video_ids.append(item['contentDetails']['videoId'])

            # Get video details
            videos_response = youtube.videos().list(
                part='snippet,statistics',
                id=','.join(video_ids)
            ).execute()

            all_videos.extend(videos_response['items'])

            next_page_token = playlist_items_response.get('nextPageToken')

            if not next_page_token:
                break
            
            if page % 5 == 0: print('page ',page)
            #if page == 5: break
            page += 1

        all_vid_details = []
        vid_detail_columns = ['vid_id', 'title', 'publishedAt', 'viewCount', 'likeCount', 'commentCount']

        print(len(all_videos))
        for item in all_videos:
            video_id = item['id']
            video_snippet = item['snippet']
            video_statistics = item['statistics']
            try:
                vid_title = video_snippet['title']
            except:
                vid_title = np.nan

            try:
                vid_upload_date = video_snippet['publishedAt']
            except:
                vid_upload_date = np.nan

            try:
                vid_view_count = video_statistics['viewCount']
            except:
                vid_view_count = np.nan
            
            try:
                vid_like = video_statistics['likeCount']
            except:
                vid_like = np.nan

            try:
                vid_comments = video_statistics['commentCount']
            except:
                vid_comments = np.nan
            single_vid_detail = [video_id, vid_title, vid_upload_date, vid_view_count, vid_like, vid_comments]
            all_vid_details.append(single_vid_detail)

            # print("Video ID:", video_id)
            # print("Title:", video_snippet['title'])
            # print("Upload Date:", video_snippet['publishedAt'])
            # print("View Count:", video_statistics['viewCount'])
            # print("Like Count:", video_statistics['likeCount'])
            # print("Comment Count:", video_statistics['commentCount'])
            # print("----------------------------------------")

        all_vid_df = pd.DataFrame(all_vid_details, columns=vid_detail_columns)
        print(all_vid_df.shape)
        print(all_vid_df.head())
        all_vid_df.to_csv('google_dev_channel_vid_details.csv', index=False)
    except HttpError as e:
        print("An HTTP error occurred:", e)


# Replace 'YOUR_API_KEY' with your actual API key
api_key = os.environ.get('YOUTUBE_API_KEY')
# Replace 'USERNAME' with the username of the channel you want to retrieve video details from
username = 'GoogleDevelopers' #CodeWithStein

get_all_video_data(username, api_key)
