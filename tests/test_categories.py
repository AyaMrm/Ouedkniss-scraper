import unittest
from unittest.mock import patch

from scraper.categories import fetch_categories, fetch_category_tree


class FetchCategoriesTest(unittest.TestCase):
    def test_fetch_categories_extracts_real_category_targets(self):
        fake_response = {
            "listingMenu": [
                {
                    "target": {
                        "__typename": "Category",
                        "id": "1",
                        "name": "Voitures",
                        "slug": "automobiles_vehicules",
                    }
                },
                {
                    "target": {
                        "__typename": "Category",
                        "id": "2",
                        "name": "Motos",
                        "slug": "motos",
                    }
                },
                {
                    "target": {"__typename": "NotACategory"}
                },
                {
                    "target": None
                },
            ]
        }

        with patch("scraper.categories.OuedknissClient") as mock_client:
            mock_client.return_value.execute.return_value = fake_response

            result = fetch_categories()

        self.assertEqual(
            result,
            [
                {"id": "1", "name": "Voitures", "slug": "automobiles_vehicules"},
                {"id": "2", "name": "Motos", "slug": "motos"},
            ],
        )

    def test_fetch_category_tree_builds_hierarchy(self):
        fake_response = {
            "listingMenu": [
                {
                    "target": {
                        "__typename": "Category",
                        "id": "10",
                        "name": "Automobiles & Véhicules",
                        "slug": "automobiles_vehicules",
                        "children": [
                            {
                                "id": "11",
                                "name": "Voitures",
                                "slug": "voitures",
                                "children": []
                            },
                            {
                                "id": "12",
                                "name": "Motos",
                                "slug": "motos",
                                "children": []
                            },
                        ],
                    }
                }
            ]
        }

        with patch("scraper.categories.OuedknissClient") as mock_client:
            mock_client.return_value.execute.return_value = fake_response

            result = fetch_category_tree()

        self.assertEqual(
            result,
            [{
                "id": "10",
                "name": "Automobiles & Véhicules",
                "slug": "automobiles_vehicules",
                "children": [
                    {"id": "11", "name": "Voitures", "slug": "voitures", "children": []},
                    {"id": "12", "name": "Motos", "slug": "motos", "children": []},
                ],
            }]
        )


if __name__ == "__main__":
    unittest.main()
