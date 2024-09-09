import unittest
import dask.dataframe as dd
import pandas as pd
from src.components.visualization_component import (
    word_frequency_chart, monthly_entry_trend_chart, top_authors_chart,
    entry_score_vs_length_chart, create_word_cloud, create_timeline
)

class TestVisualizationComponent(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        data = {
            'entiri': ['test word test', 'another word', 'test'],
            'tarih': ['2023-01-01', '2023-02-01', '2023-03-01'],
            'author': ['author1', 'author2', 'author1'],
            'score': [1, 2, 3],
            'entry_length': [10, 20, 30],
            'baslik': ['title1', 'title2', 'title3']
        }
        cls.test_df = dd.from_pandas(pd.DataFrame(data), npartitions=1)

    def test_word_frequency_chart(self):
        fig = word_frequency_chart(self.test_df)
        self.assertIsNotNone(fig)

    def test_monthly_entry_trend_chart(self):
        fig = monthly_entry_trend_chart(self.test_df)
        self.assertIsNotNone(fig)

    def test_top_authors_chart(self):
        fig = top_authors_chart(self.test_df)
        self.assertIsNotNone(fig)

    def test_entry_score_vs_length_chart(self):
        fig = entry_score_vs_length_chart(self.test_df)
        self.assertIsNotNone(fig)

    def test_create_word_cloud(self):
        fig = create_word_cloud(self.test_df)
        self.assertIsNotNone(fig)

    def test_create_timeline(self):
        fig = create_timeline(self.test_df)
        self.assertIsNotNone(fig)

if __name__ == '__main__':
    unittest.main()