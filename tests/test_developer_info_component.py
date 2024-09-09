import unittest
from unittest.mock import patch
from src.components.developer_info_component import display_developer_info

class TestDeveloperInfoComponent(unittest.TestCase):
    @patch('streamlit.markdown')
    def test_display_developer_info(self, mock_markdown):
        nickname = "geceucanpirasa"
        telegram_link = "https://t.me/asosyalarsivdev"
        display_developer_info(nickname, telegram_link)
        mock_markdown.assert_any_call("## Developer Information")
        mock_markdown.assert_any_call(f"This application was developed by **{nickname}**.")
        mock_markdown.assert_any_call(f"Contact the developer on Telegram: [{telegram_link}]({telegram_link})")

if __name__ == '__main__':
    unittest.main()