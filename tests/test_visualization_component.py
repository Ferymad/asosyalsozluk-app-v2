import unittest
import dask.dataframe as dd
import pandas as pd
from src.components.visualization_component import word_frequency_chart, monthly_entry_trend_chart

class TestVisualizationComponent(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create a sample Dask DataFrame for testing
        data = {
            'entiri': ['test word test', 'another word', 'test'],
            'tarih': ['2023-01-01', '2023-02-01', '2023-03-01']
        }
        cls.test_df = dd.from_pandas(pd.DataFrame(data), npartitions=1)

    def test_word_frequency_chart(self):
        fig = word_frequency_chart(self.test_df)
        self.assertIsNotNone(fig)
        self.assertEqual(fig.layout.title.text, 'En Sık Kullanılan Kelimeler')

    def test_monthly_entry_trend_chart(self):
        fig = monthly_entry_trend_chart(self.test_df)
        self.assertIsNotNone(fig)
        self.assertEqual(fig.layout.title.text, 'Aylık Girdi Sayısı Trendi')

if __name__ == '__main__':
    unittest.main()