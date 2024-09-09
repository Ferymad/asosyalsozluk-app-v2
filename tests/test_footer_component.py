import unittest
from unittest.mock import patch
from src.components.footer_component import display_footer

class TestFooterComponent(unittest.TestCase):
    @patch('streamlit.markdown')
    def test_display_footer(self, mock_markdown):
        display_footer()
        mock_markdown.assert_called_once_with("""
    ---
    ### Developer Information
    This application was developed by **geceucanpirasa**.
    
    Contact the developer on Telegram: [@asosyalarsivdev](https://t.me/asosyalarsivdev)
    """)

if __name__ == '__main__':
    unittest.main()