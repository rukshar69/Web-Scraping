import streamlit as st
import json; import pandas as pd; import re
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt

st.header('[LuLu Electronics Products](https://www.luluhypermarket.com/en-ae/electronics) Analysis')
st.write('The info of products are scraped using [scrapy](https://scrapy.org/)')

st.cache_data()
def load_data():
    with open('lulu_scraping/lulu_scraper/lulu_scraper/products_desc.json') as file:
        prd_details = json.load(file)
    return prd_details

def clean_price_data(item_prices): 
    #item_prices: list of prices in the format 'AED 3,900.00'
    numbers = []

    for string in item_prices:
        number = re.sub(r'\.0*$', '', string)  # Remove decimal point and trailing zeros
        number = re.sub(r'[^0-9]', '', number)  # Remove non-digit characters
        
        numbers.append(int(number))

    return numbers

#concatenates prd details to create single text for generating word cloud
def generate_text_from_product_details(prd_list):
    #prd_list-> list of dictionary with product details
    final_text = ''
    for prd in prd_list:
        item_summary = prd['item_summary']
        concatenated_string = ' '.join(item_summary.values())
        final_text = final_text + ' '+concatenated_string
    return final_text

def generate_wordcloud(text):
    wordcloud = WordCloud().generate(text)

    # Display the word cloud using matplotlib
    fig, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig)

prd_details = load_data()
st.write(prd_details)

#************************************************************************************************************
st.header('Category Distribution')
sub_categories = [d['sub_cat'] for d in prd_details]
# Create a pandas Series from the sub_categories list
sub_category_series = pd.Series(sub_categories)

# Create a dataframe with 'sub_category' and 'count' columns
df = pd.DataFrame({'sub_category': sub_category_series.unique(), 'count': sub_category_series.value_counts()})

# Sort the dataframe by sub_category name
df = df.sort_values('sub_category').reset_index(drop=True)

fig = px.bar(df, x='sub_category', y='count', title='Sub-Category Counts')

st.plotly_chart(fig)

#************************************************************************************************************
st.header('Price Analysis')
prices = [d['item_price'] for d in prd_details] #get the prices
cleaned_prices = clean_price_data(prices) #clean the price strings
#DRAW DIST PLOT
prices_df = pd.DataFrame({'Price': cleaned_prices})
fig = px.histogram(prices_df, x='Price', nbins=100, title='Price Distribution', )
fig.update_traces(marker_color='green')  # Set marker color to green
st.plotly_chart(fig)

#************************************************************************************************************
st.header('Price Analysis by Category')
unique_sub_categories = list(set(sub_categories))
selected_option = st.selectbox('Select a category', unique_sub_categories)
filtered_prd_details =  list(filter(lambda d: d['sub_cat'] == selected_option, prd_details))
filtered_prices =  [d['item_price'] for d in filtered_prd_details] 
filtered_cleaned_prices = clean_price_data(filtered_prices)
filtered_prices_df = pd.DataFrame({'Price': filtered_cleaned_prices})
fig = px.histogram(filtered_prices_df, x='Price', nbins=100, title=selected_option+ ' Price Distribution', )
fig.update_traces(marker_color='purple')  # Set marker color to green
st.plotly_chart(fig)

## prd details concatenated 
st.write('### Wordcloud for '+selected_option)
concatenated_summary = generate_text_from_product_details(filtered_prd_details)
generate_wordcloud(text=concatenated_summary)
