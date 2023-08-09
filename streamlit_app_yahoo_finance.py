import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.subplots as sp
import plotly.graph_objects as go

@st.cache_data()
def load_data():
    # Load your CSV file into a Pandas DataFrame
    df = pd.read_csv('./yahoo_finance_stocks/stocks_info.csv')
    return df 
df = load_data()

st.title('Stock Market Data Visualization')
st.write('The data is collected from Yahoo Finance on 1st August, 2023. This is collected across \
         different sectors. The CSV file contains the following columns: \
         name, ticker, intraday_price, sector,	market_cap,	pe_ratio_ttm,	percent_change,	price_change,volume, avg_vol_3_month')
st.write('An example page from the data is collected: [https://finance.yahoo.com/screener/predefined/ms_basic_materials?offset=0&count=100](https://finance.yahoo.com/screener/predefined/ms_basic_materials?offset=0&count=100)')


st.header('Top 10 Companies Based on Selected Sector and Column')
st.write('Showing Top 10 companies across different sectors based on the chosen metric')

selected_sector = st.selectbox('Select Sector', df['sector'].unique())
selected_column = st.selectbox('Select Column', ['avg_vol_3_month', 'intraday_price', 'market_cap', 'pe_ratio_ttm', 'percent_change', 'price_change', 'volume'])

# Filter data based on selected sector
filtered_data = df[df['sector'] == selected_sector]

# Main content
st.write(f'Showing data for sector: {selected_sector} and column: {selected_column}')

# Get the top 10 companies based on the selected column
top_10_companies = filtered_data.nlargest(10, selected_column)[['name', 'ticker', selected_column]]
st.table(top_10_companies)

st.write(f'### Showing data distribution and boxplot for sector: {selected_sector} and column: {selected_column}')
# Create subplots
fig = sp.make_subplots(rows=1, cols=2, subplot_titles=("Data Distribution", "Boxplot"))

# Add histogram to the first subplot
fig.add_trace(px.histogram(filtered_data, x=selected_column, title="Data Distribution").data[0], row=1, col=1)

# Add boxplot to the second subplot
fig.add_trace(px.box(filtered_data, y=selected_column, title="Boxplot").data[0], row=1, col=2)

# Update layout
fig.update_layout(showlegend=False)
st.plotly_chart(fig)

# Create dynamic numerical ranges based on the selected column
num_ranges = 6  # Number of ranges
min_val = filtered_data[selected_column].min()
max_val = filtered_data[selected_column].max()
range_values = [(min_val + i * (max_val - min_val) / num_ranges) for i in range(num_ranges + 1)]
range_labels = [f'{range_values[i]:.2f} - {range_values[i+1]:.2f}' for i in range(num_ranges)]
filtered_data['range'] = pd.cut(filtered_data[selected_column], bins=range_values, labels=range_labels)

# Main content
st.write('### Donut Chart: Distribution by Numerical Range')
st.write(f'Showing the distribution within sector: {selected_sector} based on {selected_column} ranges')

# Create a donut chart
if 'sector' in df.columns and 'range' in filtered_data.columns:
    fig = px.pie(
        filtered_data,
        names='range',
        title=f'Distribution by {selected_column} Range',
        hole=0.5  # Hole to make it a donut chart
    )
    st.plotly_chart(fig)
else:
    st.write('Selected dataset does not contain required columns.')


st.write('### Scatter Plot: Market Cap vs. PE Ratio')
st.write(f'Showing scatter plot for Market Cap vs. PE Ratio in sector: {selected_sector}')

# Create scatter plot
if 'market_cap' in df.columns and 'pe_ratio_ttm' in df.columns and 'avg_vol_3_month' in df.columns:
    fig = px.scatter(
        filtered_data,
        x='market_cap',
        y='pe_ratio_ttm',
        size='avg_vol_3_month',
        hover_name='name',
        title='Scatter Plot: Market Cap vs. PE Ratio',
        labels={'market_cap': 'Market Cap', 'pe_ratio_ttm': 'PE Ratio', 'avg_vol_3_month': 'Avg. Volume'}
    )
    fig.update_traces(marker=dict(line=dict(width=0.5, color='DarkSlateGrey')))
    st.plotly_chart(fig)
else:
    st.write('Selected sector does not contain required columns.')

st.write('### Pair Plot: Scatter Matrix')
st.write(f'Showing relationships between numerical columns for sector: {selected_sector}')

# Create scatter matrix using Plotly
if 'sector' in df.columns and 'avg_vol_3_month' in df.columns and 'intraday_price' in df.columns and 'market_cap' in df.columns and 'pe_ratio_ttm' in df.columns:
    numerical_columns = ['avg_vol_3_month', 'intraday_price', 'market_cap', 'pe_ratio_ttm']
    fig = px.scatter_matrix(filtered_data, dimensions=numerical_columns, title='Scatter Matrix')
    st.plotly_chart(fig)
else:
    st.write('Selected dataset does not contain required columns.')

st.write(f'### Violin Plot: Distribution of {selected_column} by Sector')
st.write(f'Showing the distribution of {selected_column} across different sectors')

# Create a violin plot
if 'sector' in df.columns and selected_column in df.columns:
    fig = px.violin(df, x='sector', y=selected_column, box=True, title=f'Distribution of {selected_column} by Sector')
    st.plotly_chart(fig)
else:
    st.write('Selected dataset does not contain required columns.')


st.header('Bar Chart: Average Volume by Sector')
st.write('Comparing the average volume for different sectors')

# Create a bar chart
if 'sector' in df.columns and 'avg_vol_3_month' in df.columns:
    sector_avg_volume = df.groupby('sector')['avg_vol_3_month'].mean().reset_index()
    fig = px.bar(
        sector_avg_volume,
        x='sector',
        y='avg_vol_3_month',
        title='Average Volume by Sector',
        labels={'sector': 'Sector', 'avg_vol_3_month': 'Average Volume'}
    )
    st.plotly_chart(fig)
else:
    st.write('Selected dataset does not contain required columns.')

st.header('Pie Chart: Distribution of Companies by Sector')
st.write('Showing the percentage composition of companies across different sectors')

# Create a pie chart
if 'sector' in df.columns:
    sector_distribution = df['sector'].value_counts().reset_index()
    sector_distribution.columns = ['sector', 'count']
    fig = px.pie(
        sector_distribution,
        values='count',
        names='sector',
        title='Distribution of Companies by Sector'
    )
    st.plotly_chart(fig)
else:
    st.write('Selected dataset does not contain required columns.')

# Main content
st.header('Heatmap: Correlation Matrix')
st.write('Showing the correlation matrix between numerical columns')

# Calculate the correlation matrix
numerical_columns = ['avg_vol_3_month', 'intraday_price', 'market_cap', 'pe_ratio_ttm', 'percent_change', 'price_change', 'volume']
correlation_matrix = df[numerical_columns].corr()

# Create a heatmap
fig = px.imshow(correlation_matrix, labels=dict(x="Columns", y="Columns", color="Correlation"))
fig.update_xaxes(side="top")
st.plotly_chart(fig)


# # Main content
# st.write(f'Showing data for sector: {selected_sector}')

# # Create a plot based on the selected column
# if selected_column in ['avg_vol_3_month', 'intraday_price', 'market_cap', 'pe_ratio_ttm', 'percent_change', 'price_change', 'volume']:
#     st.line_chart(filtered_data[selected_column])
# else:
#     st.write('Select a valid column from the dropdown.')

# # You can add more visualizations here based on the selected column

# # Optional: Display a table with the filtered data
# st.write(filtered_data)

