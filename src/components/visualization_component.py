import streamlit as st
import dask.dataframe as dd
import plotly.graph_objs as go
import plotly.express as px
from collections import Counter
import nltk
from nltk.corpus import stopwords

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

def run_visualization_component(dask_df: dd.DataFrame):
    st.subheader("Data Visualization")
    
    # Visualization options
    chart_type = st.selectbox(
        "Select Chart Type",
        ["Monthly Entry Trend", "Word Frequency"]
    )

    # Display the selected chart
    if chart_type == "Monthly Entry Trend":
        with st.spinner("Loading chart..."):
            st.plotly_chart(monthly_entry_trend_chart(dask_df))
    elif chart_type == "Word Frequency":
        with st.spinner("Loading chart..."):
            st.plotly_chart(word_frequency_chart(dask_df))