import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import plotly.express as px

st.cache_data()
def load_data():
    channel_stats_df = pd.read_csv('./YoutubeScrapper/data/channel_stats.csv')
    vids_df = pd.read_csv('./YoutubeScrapper/data/google_dev_vid_details_cleaned.csv')
    # Convert the date column to a datetime object
    vids_df["uploaded"] = pd.to_datetime(vids_df["uploaded"])
    #vids_df['uploaded'] = vids_df['uploaded'].dt.date
    return channel_stats_df, vids_df

def total_likes(video_df):
    total_like_amount = video_df['likes'].sum()
    return total_like_amount

def draw_scatter_plot(video_df):
    # Create the scatter plot
    #drop rows with na values
    video_df = video_df.dropna(subset=["views", "likes"])  
    scatter_trace = go.Scatter(
        x=video_df['likes'],
        y=video_df['views'],
        mode='markers',
        name='Data Points'
    )

    # Calculate the regression line
    slope, intercept = np.polyfit(video_df['likes'], video_df['views'], 1)
    regression_line = slope * video_df['likes'] + intercept

    # Create the line trace for the regression line
    line_trace = go.Scatter(
        x=video_df['likes'],
        y=regression_line,
        mode='lines',
        name='Regression Line'
    )

    # Combine the scatter plot and the line trace
    data = [scatter_trace, line_trace]

    # Create the layout
    layout = go.Layout(
        title='Scatter Plot with Regression Line',
        xaxis=dict(title='Likes'),
        yaxis=dict(title='Views'),
    )

    # Create the figure
    fig = go.Figure(data=data, layout=layout)

    # Display the plot
    st.plotly_chart(fig)

def draw_stat_by_year(video_df):
    # Get the year for each video
    video_df["year"] = video_df["uploaded"].dt.year

    # Calculate the total views and likes by year
    total_views_by_year = video_df.groupby("year")["views"].sum()
    total_likes_by_year = video_df.groupby("year")["likes"].sum()
    #st.write(video_df["year"])
    #st.write(total_views_by_year.values)

    #PLOT VIEWS BY YEAR
    x = total_views_by_year.index
    y = total_views_by_year.values

    # Create the bar plot
    fig = go.Figure(data=go.Bar(x=x, y=y,  marker=dict(color='green')))

    # Update the layout
    fig.update_layout(
        title='Views Bar Plot',
        xaxis=dict(title='Years'),
        yaxis=dict(title='Values'),
    )
    st.plotly_chart(fig)

    # PLOT LIKES BY YEAR
    x = total_likes_by_year.index
    y = total_likes_by_year.values

    # Create the bar plot
    fig = go.Figure(data=go.Bar(x=x, y=y))

    # Update the layout
    fig.update_layout(
        title='Likes Bar Plot',
        xaxis=dict(title='Years'),
        yaxis=dict(title='Values'),
    )
    st.plotly_chart(fig)

def basic_info(channel_stats_df):
    #subscribers ,videos, views, likes, avg view/vid, avg like/vid
    st.write('Subscribers: **'+str(channel_stats_df['subscribers'].values[0]) + '**')
    st.write('Total Views: **'+str(channel_stats_df['views'].values[0]) + '**')
    st.write('Avg. Views/Video: **'+str(round(channel_stats_df['views'].values[0]/channel_stats_df['videos'].values[0], 2)) + '**')
    st.write('Total Videos: **'+str(channel_stats_df['videos'].values[0]) + '**')
    st.write('Total Likes: **'+str(total_likes(vids_df))+'**')
    st.write('Avg. Likes/Video: **'+str(round(total_likes(vids_df)/channel_stats_df['videos'].values[0], 2)) + '**')
    st.write('[As of **' + channel_stats_df['date'].values[0]+ '** ]')

def videos_by_upload_date(video_df):
    video_df['only_date'] = video_df['uploaded'].dt.date
    vids_by_date = video_df.groupby(["only_date"])["title"].count()

    #PLOT VIEWS BY YEAR
    x = vids_by_date.index
    y = vids_by_date.values

    # Create the bar plot
    fig = go.Figure(data=go.Bar(x=x, y=y,  marker=dict(color='purple')))

    # Update the layout
    fig.update_layout(
        title='Video Uploaded Chart',
        xaxis=dict(title='Date'),
        yaxis=dict(title='No. of Vids'),
    )
    st.plotly_chart(fig)


channel_stats_df, vids_df = load_data()
st.header('Basic Channel Info for ['+channel_stats_df['channelname'].values[0]+'](https://www.youtube.com/@GoogleDevelopers)')
basic_info(channel_stats_df=channel_stats_df)

st.header('Video Data')

st.write(vids_df.drop("vid_id", axis=1).sort_values("views", ascending=False))

st.header('Distribution Plot')

# Create a selector
distplot_option = st.selectbox(
    "Option",
    ("Views", "Likes"),
)

if distplot_option == 'Views':
    # Create a distribution plot
    fig = px.histogram(vids_df['views'], title="Views Distribution Plot")
    # Show the plot in Streamlit
    st.plotly_chart(fig)

    # Create a boxplot
    fig = px.box(vids_df['views'], title="Views Box Plot")
    st.plotly_chart(fig)
else:
    # Create a distribution plot
    fig = px.histogram(vids_df['likes'], title="likes Distribution Plot")
    # Change the color of the plot to green
    fig.update_traces(marker_color="green")
    # Show the plot in Streamlit
    st.plotly_chart(fig)

    # Create a boxplot
    fig = px.box(vids_df['views'], title="likes Box Plot")
    fig.update_traces(marker_color="green")
    st.plotly_chart(fig)
st.write('Both the *views* and *likes* distribution plots are heavily skewed with long tails. Most videos get smaller number of likes and views while a few \
         vids get high likes and views')

st.header('Scatter Plot Views vs. Likes')
# Create a scatter plot
draw_scatter_plot(vids_df)
st.write('Despite some outliers where some videos have garnered high views with low likes, most data points exhibit a linear relationship between views and likes')

st.header('Views/Likes by year')
draw_stat_by_year(vids_df)

st.header('Time Series Plot for Videos vs Upload Date')
videos_by_upload_date(vids_df)
st.write('With occasional spikes in video uploads, the densest period of video upload seems to be from *2012 to mid 2016*.\
         After that video upload was less but appears to be consistent. Before 2012, video uploads are quite low. The highest peaks of video uploads prior to 2020 are observed in mostly May and sometimes June.\
         After 2020, the spikes in video uploads occur in regular intervals throughout the period. ')


#time series plot for number of videos uploaded vs upload date