import streamlit as st
import dask.dataframe as dd
import plotly.graph_objs as go
import plotly.express as px
import plotly.figure_factory as ff
from collections import Counter
import nltk
from nltk.corpus import stopwords
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd

# Download NLTK data
nltk.download('stopwords', quiet=True)

# Modify the cache decorator to work with testing
def cacheable_word_frequency_chart(dask_df: dd.DataFrame) -> go.Figure:
    stop_words = set(stopwords.words('turkish'))
    words = dask_df['entiri'].str.cat(sep=' ').compute().lower().split()
    word_freq = Counter(word for word in words if word not in stop_words)
    top_words = dict(word_freq.most_common(20))
    
    fig = go.Figure(go.Bar(x=list(top_words.keys()), y=list(top_words.values())))
    fig.update_layout(
        title='En Sık Kullanılan Kelimeler',
        xaxis_title='Kelime',
        yaxis_title='Frekans',
        width=600,
        height=400
    )
    
    return fig

@st.cache_data(hash_funcs={dd.DataFrame: lambda _: None})
def word_frequency_chart(dask_df: dd.DataFrame) -> go.Figure:
    return cacheable_word_frequency_chart(dask_df)

# Modify the cache decorator to work with testing
def cacheable_monthly_entry_trend_chart(dask_df: dd.DataFrame) -> go.Figure:
    # Convert 'tarih' column to datetime
    dask_df['tarih'] = dd.to_datetime(dask_df['tarih'], errors='coerce')
    
    # Group by month and compute the size
    monthly_counts = dask_df.groupby(dask_df['tarih'].dt.to_period('M')).size().compute()
    monthly_counts.index = monthly_counts.index.to_timestamp()
    
    fig = px.line(
        x=monthly_counts.index,
        y=monthly_counts.values,
        title='Aylık Girdi Sayısı Trendi'
    )
    fig.update_layout(
        xaxis_title='Tarih',
        yaxis_title='Girdi Sayısı',
        width=600,
        height=400
    )
    return fig

@st.cache_data(hash_funcs={dd.DataFrame: lambda _: None})
def monthly_entry_trend_chart(dask_df: dd.DataFrame) -> go.Figure:
    return cacheable_monthly_entry_trend_chart(dask_df)

def top_authors_chart(dask_df: dd.DataFrame) -> go.Figure:
    author_counts = dask_df['author'].value_counts().nlargest(10).compute()
    fig = px.bar(x=author_counts.index, y=author_counts.values, title='Top 10 Authors')
    fig.update_layout(xaxis_title='Author', yaxis_title='Number of Entries', width=600, height=400)
    return fig

def entry_score_vs_length_chart(dask_df: dd.DataFrame) -> go.Figure:
    # Ensure to sample the DataFrame after selecting necessary columns
    sample = dask_df[['entiri', 'skor', 'author', 'baslik']].sample(frac=0.1).compute()  # Sample 10% of data for performance
    sample['entry_length'] = sample['entiri'].str.len()

    fig = px.scatter(sample, x='entry_length', y='skor', hover_data=['author', 'baslik'],
                     title='Entry Score vs Length')
    fig.update_layout(width=600, height=400)
    return fig

def create_word_cloud(dask_df: dd.DataFrame) -> plt.Figure:
    all_text = " ".join(dask_df['entiri'].compute())
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_text)
    fig, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    return fig

def create_timeline(dask_df: dd.DataFrame) -> go.Figure:
    df = dask_df.compute()
    df['tarih'] = pd.to_datetime(df['tarih'])
    fig = ff.create_gantt(df, x_start='tarih', x_end='tarih', y='baslik', 
                          show_colorbar=True, group_tasks=True)
    fig.update_layout(title='Entry Timeline', width=800, height=400)
    return fig

def run_visualization_component(dask_df: dd.DataFrame):
    st.subheader("Data Visualization")
    
    # Visualization options
    chart_type = st.selectbox(
        "Select Chart Type",
        ["Monthly Entry Trend", "Word Frequency", "Top Authors", "Entry Score vs Length", "Word Cloud", "Timeline"]
    )

    # Display the selected chart
    if chart_type == "Monthly Entry Trend":
        with st.spinner("Loading chart..."):
            st.plotly_chart(monthly_entry_trend_chart(dask_df))
    elif chart_type == "Word Frequency":
        with st.spinner("Loading chart..."):
            st.plotly_chart(word_frequency_chart(dask_df))
    elif chart_type == "Top Authors":
        with st.spinner("Loading chart..."):
            st.plotly_chart(top_authors_chart(dask_df))
    elif chart_type == "Entry Score vs Length":
        with st.spinner("Loading chart..."):
            st.plotly_chart(entry_score_vs_length_chart(dask_df))
    elif chart_type == "Word Cloud":
        with st.spinner("Generating word cloud..."):
            st.pyplot(create_word_cloud(dask_df))
    elif chart_type == "Timeline":
        with st.spinner("Creating timeline..."):
            st.plotly_chart(create_timeline(dask_df))