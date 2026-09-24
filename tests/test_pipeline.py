import unittest
from unittest.mock import patch

from scraper.pipeline import scrape_category


class ScrapeCategoryTest(unittest.TestCase):
    @patch("scraper.pipeline.scrape_page")
    def test_scrape_category_follows_all_pages(self, mock_scrape_page):
        mock_scrape_page.side_effect = [
            {
                "data": [{"id": "1"}],
                "pagination": {"hasMorePages": True},
                "errors": [],
            },
            {
                "data": [{"id": "2"}],
                "pagination": {"hasMorePages": False},
                "errors": [],
            },
        ]

        result = scrape_category("cars", max_pages=None, count=48, client=object())

        self.assertEqual([item["id"] for item in result["data"]], ["1", "2"])
        self.assertEqual(mock_scrape_page.call_count, 2)

    @patch("scraper.pipeline.scrape_page")
    def test_scrape_category_deduplicates_ids(self, mock_scrape_page):
        mock_scrape_page.side_effect = [
            {
                "data": [{"id": "1"}, {"id": "2"}],
                "pagination": {"hasMorePages": False},
                "errors": [],
            }
        ]

        result = scrape_category("cars", max_pages=1, client=object())

        self.assertEqual([item["id"] for item in result["data"]], ["1", "2"])
        self.assertEqual(result["duplicates"], 0)


if __name__ == "__main__":
    unittest.main()