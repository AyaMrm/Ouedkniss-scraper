import json
from unittest import result

from categories.cars import CATEGORY
from scraper.pipeline import scrape_page
from scraper.pipeline import scrape_category

def main():

    result = scrape_category(
        category_slug=CATEGORY["slug"],
        max_pages=3,
        count=48
    )

    output = {
        "category": CATEGORY["name"],
        "category_slug": CATEGORY["slug"],
        "pages": 3,
        "count": len(result["data"]),
        "duplicates": result["duplicates"],
        "errors": result["errors"],
        "announcements": result["data"]
    }

    with open(
        "output/cars.json",
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            output,
            file,
            ensure_ascii=False,
            indent=4
        )

    print()
    print("=" * 50)
    print(f"Saved {len(result['data'])} announcements")
    print(f"Duplicates skipped: {result['duplicates']}")
    print(f"Errors: {len(result['errors'])}")
    print("=" * 50)


if __name__ == "__main__":
    main()