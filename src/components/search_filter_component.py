import streamlit as st
import dask.dataframe as dd
from typing import Dict, Any
from datetime import datetime, timezone
import math
import pandas as pd

def search_filter_sidebar(dask_df: dd.DataFrame) -> Dict[str, Any]:
    st.sidebar.header("Search and Filter")

    # Compute min and max dates from the 'tarih' column
    min_date = dask_df['tarih'].min().compute()
    max_date = dask_df['tarih'].max().compute()

    # Convert to datetime.date for the date_input widget
    min_date = pd.to_datetime(min_date).date()
    max_date = pd.to_datetime(max_date).date()

    search_term = st.sidebar.text_input("Search entries")
    date_range = st.sidebar.date_input("Date range", value=(min_date, max_date))
    show_deleted = st.sidebar.checkbox("Show deleted entries", value=False)
    entries_per_page = st.sidebar.selectbox("Entries per page", options=[10, 20, 50, 100], index=0)

    return {
        "search_term": search_term,
        "start_date": datetime.combine(date_range[0], datetime.min.time()).replace(tzinfo=timezone.utc),
        "end_date": datetime.combine(date_range[1], datetime.max.time()).replace(tzinfo=timezone.utc),
        "show_deleted": show_deleted,
        "entries_per_page": entries_per_page
    }

def run_search_filter_component(dask_df: dd.DataFrame):
    filter_options = search_filter_sidebar(dask_df)
    search_query = filter_options["search_term"]
    entries_per_page = filter_options["entries_per_page"]

    # Debugging: Print initial number of entries
    initial_entries = len(dask_df)
    st.write(f"Initial entries: {initial_entries}")

    # Ensure 'tarih' column is datetime with timezone information
    dask_df['tarih'] = dd.to_datetime(dask_df['tarih'], errors='coerce').dt.tz_localize(None).dt.tz_localize('UTC')

    # Apply date filters
    start_date = pd.Timestamp(filter_options["start_date"])
    end_date = pd.Timestamp(filter_options["end_date"])
    filtered_df = dask_df[
        (dask_df['tarih'] >= start_date) &
        (dask_df['tarih'] <= end_date)
    ]

    # Debugging: Print number of entries after date filtering
    date_filtered_entries = len(filtered_df)
    st.write(f"Entries after date filtering: {date_filtered_entries}")

    # Apply deletion filter
    if not filter_options["show_deleted"]:
        filtered_df = filtered_df[~filtered_df['silinmis']]

    # Debugging: Print number of entries after deletion filter
    deletion_filtered_entries = len(filtered_df)
    st.write(f"Entries after deletion filter: {deletion_filtered_entries}")

    # Apply search query filter
    if search_query:
        filtered_df = filtered_df[
            filtered_df['baslik'].astype(str).str.contains(search_query, case=False, na=False) |
            filtered_df['entiri'].astype(str).str.contains(search_query, case=False, na=False)
        ]

    # Debugging: Print number of entries after search filter
    search_filtered_entries = len(filtered_df)
    st.write(f"Entries after search filtering: {search_filtered_entries}")

    total_entries = len(filtered_df)
    total_pages = math.ceil(total_entries / entries_per_page)
    st.write(f"Total entries after filtering: {total_entries}")

    # Pagination controls
    col1, col2, col3 = st.columns([1,2,1])
    with col1:
        if st.button("Previous") and st.session_state.current_page > 1:
            st.session_state.current_page -= 1
    with col2:
        st.write(f"Page {st.session_state.current_page} of {total_pages}")
    with col3:
        if st.button("Next") and st.session_state.current_page < total_pages:
            st.session_state.current_page += 1

    # Load entries for the current page
    start_idx = (st.session_state.current_page - 1) * entries_per_page
    end_idx = start_idx + entries_per_page

    # Compute the Dask DataFrame to a Pandas DataFrame for pagination
    page_entries = filtered_df.compute().iloc[start_idx:end_idx]

    # Display entries
    for _, entry in page_entries.iterrows():
        st.markdown(f"### {entry['baslik']}")
        st.write(entry['entiri'])
        st.write(f"Score: {entry['skor']} | Date: {entry['tarih']}")
        if entry['silinmis']:
            st.write("(Deleted)")
        st.markdown("---")