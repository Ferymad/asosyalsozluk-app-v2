import streamlit as st
import dask.dataframe as dd
from typing import List, Dict, Any, Optional
from components.upload_component import upload_csv
from components.search_filter_component import run_search_filter_component
from components.visualization_component import run_visualization_component
from services.csv_to_json import process_uploaded_file
from utils.data_validation import validate_and_clean_data
from components import display_developer_info, display_footer

# Initialize session state
if 'dask_df' not in st.session_state:
    st.session_state.dask_df = None
if 'current_page' not in st.session_state:
    st.session_state.current_page = 1

@st.cache_data
def load_data(file_path: str) -> dd.DataFrame:
    return dd.read_csv(file_path)

def main() -> None:
    st.title("Asosyal Sözlük Veri Analizi")

    uploaded_file = st.file_uploader("CSV dosyasını yükleyin", type="csv")

    if uploaded_file is not None:
        df = upload_csv(uploaded_file)
        if df is not None and not df.empty:
            # Convert pandas DataFrame to Dask DataFrame
            dask_df = dd.from_pandas(df, npartitions=1)
            
            # Store the Dask DataFrame in session state
            st.session_state.dask_df = dask_df
            
            total_entries = len(dask_df)
            st.write(f"Total entries: {total_entries}")
            
            # Data Analysis and Visualization Section
            st.header("Veri Görselleştirme")
            run_visualization_component(st.session_state.dask_df)
            
            # Entries Display Section
            st.header("Girdiler")
            run_search_filter_component(st.session_state.dask_df)
            
            # Display developer information
            display_developer_info(nickname="geceucanpirasa", telegram_link="https://t.me/asosyalarsivdev")
        else:
            st.error("Failed to process the uploaded file.")
    else:
        st.warning("Please upload a CSV file to begin.")

    # Display footer with developer information
    display_footer()

if __name__ == "__main__":
    main()