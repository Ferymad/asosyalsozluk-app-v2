import streamlit as st

def display_developer_info(nickname: str, telegram_link: str):
    st.markdown("## Developer Information")
    st.markdown(f"This application was developed by **{nickname}**.")
    st.markdown(f"Contact the developer on Telegram: [{telegram_link}]({telegram_link})")