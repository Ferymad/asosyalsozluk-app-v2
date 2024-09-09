import streamlit as st
import dask.dataframe as dd
from typing import List, Dict, Any, Optional
from components.upload_component import upload_csv
from components.search_filter_component import run_search_filter_component
from components.visualization_component import run_visualization_component

# ... (rest of your app code)

# At the bottom of your main app file or in your footer component
st.markdown("""
---
### Contact the Developer
* Telegram: [@your_telegram_username](https://t.me/asosyalarsivdev)
""")

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
        else:
            st.error("Failed to process the uploaded file.")
    else:
        st.warning("Please upload a CSV file to begin.")

if __name__ == "__main__":
    main()

