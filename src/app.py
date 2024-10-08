import streamlit as st
import json
import os
from services.csv_to_json import process_uploaded_file
from components.display_component import display_entries
from components.search_filter_component import run_search_filter_component, search_filter_sidebar
from components.visualization_component import run_visualization_component, prepare_data
import math
import csv
import pandas as pd
from itertools import islice
from datetime import datetime, timedelta
import pytz
import tempfile
from importlib import import_module

# Initialize session state
if 'json_data' not in st.session_state:
    st.session_state.json_data = None

@st.cache_data
def process_data(file_path):
    df = pd.read_csv(file_path, encoding='utf-8')
    return df.to_dict('records')

def save_uploaded_file(uploaded_file):
    """Save the uploaded file to a temporary directory."""
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            return tmp_file.name
    except Exception as e:
        st.error(f"Error saving file: {e}")
        return None

def load_component(component_name):
    module = import_module(f"components.{component_name}")
    return getattr(module, f"run_{component_name}")

# Main app logic
def main():
    st.title("Asosyal Sözlük Veri Analizi")

    uploaded_file = st.file_uploader("CSV dosyasını yükleyin", type="csv")

    if uploaded_file is not None:
        file_path = save_uploaded_file(uploaded_file)
        if file_path:
            entries = process_data(file_path)
            st.write(f"Number of entries loaded: {len(entries)}")
            
            # Data Analysis and Visualization Section
            st.header("Veri Görselleştirme")
            visualization_component = load_component("visualization_component")
            visualization_component(entries)
            
            # Entries Display Section
            st.header("Girdiler")
            search_filter_component = load_component("search_filter_component")
            search_filter_component(entries)

    else:
        st.warning("Please upload a CSV file to begin.")

if __name__ == "__main__":
    main()