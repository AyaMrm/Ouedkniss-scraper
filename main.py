import json
import sys

from scraper.categories import fetch_categories, fetch_category_tree
from scraper.graphql.client import OuedknissClient
from scraper.pipeline import scrape_category


def iter_tree_paths(nodes, parent_path=()):
    for index, node in enumerate(nodes, start=1):
        path = parent_path + (index,)
        yield path, node

        for child_path, child in iter_tree_paths(node.get("children", []), path):
            yield child_path, child


def find_node_by_path(nodes, path):
    if not path:
        return None

    current = nodes[path[0] - 1]

    if len(path) == 1:
        return current

    return find_node_by_path(current.get("children", []), path[1:])


def print_category_menu(categories):
    print("\nAvailable categories:")
    print("-" * 70)

    for path, category in iter_tree_paths(categories):
        indent = "  " * (len(path) - 1)
        label = ".".join(str(item) for item in path)
        print(f"{indent}{label}. {category['name']} ({category['slug']})")

    print("-" * 70)
    print("Choose a category by number or by hierarchical path")
    print("Examples: '2', '2.1', '2.2'")
    print("Type 'q' to quit")
    print("Type 'all' to scrape all categories")
    print("Type 'quick' to scrape the first 3 categories")


def select_category(categories):
    print_category_menu(categories)

    while True:
        choice = input("\nYour choice: ").strip().lower()

        if choice in {"q", "quit", "exit"}:
            raise SystemExit(0)

        if choice == "all":
            return "all"

        if choice == "quick":
            return "quick"

        try:
            path = tuple(int(part) for part in choice.split("."))
        except ValueError:
            print("Invalid choice. Enter a number like '2' or a path like '2.1'.")
            continue

        selected = find_node_by_path(categories, path)
        if selected is not None:
            return selected

        print("This path does not exist. Please choose a valid category.")


def run_single_category(category, max_pages=1, count=5):
    category_name = category["name"]
    category_slug = category["slug"]

    print(f"\n=== {category_name} ({category_slug}) ===")

    result = scrape_category(
        category_slug=category_slug,
        max_pages=max_pages,
        count=count,
    )

    output = {
        "category": category_name,
        "category_slug": category_slug,
        "pages": max_pages,
        "count": len(result["data"]),
        "duplicates": result["duplicates"],
        "errors": result["errors"],
        "announcements": result["data"],
    }

    with open("output/selected_category.json", "w", encoding="utf-8") as file:
        json.dump(output, file, ensure_ascii=False, indent=4)

    print(f"\nSaved {len(result['data'])} announcements for {category_name}")
    print(f"Duplicates skipped: {result['duplicates']}")
    print(f"Errors: {len(result['errors'])}")


def run_quick_test():
    categories = fetch_categories()
    selected = categories[:3]

    print("Quick mode: scraping only the first 3 categories")

    all_announcements = []
    all_errors = []
    total_duplicates = 0

    for category in selected:
        category_name = category["name"]
        category_slug = category["slug"]

        print(f"\n=== {category_name} ({category_slug}) ===")

        result = scrape_category(
            category_slug=category_slug,
            max_pages=1,
            count=5,
        )

        all_announcements.extend(result["data"])
        all_errors.extend(result["errors"])
        total_duplicates += result["duplicates"]

    output = {
        "categories_count": len(selected),
        "total_announcements": len(all_announcements),
        "duplicates": total_duplicates,
        "errors": all_errors,
        "announcements": all_announcements,
    }

    with open("output/quick_test.json", "w", encoding="utf-8") as file:
        json.dump(output, file, ensure_ascii=False, indent=4)

    print(f"\nQuick test finished: {len(all_announcements)} announcements scraped")
    print(f"Duplicates: {total_duplicates}")
    print(f"Errors: {len(all_errors)}")


def run_full_mode():
    categories = fetch_categories()

    if not categories:
        raise RuntimeError("No categories returned by the Ouedkniss menu API.")

    all_announcements = []
    all_errors = []
    total_duplicates = 0
    client = OuedknissClient()
    unique_announcements = {}

    for category in categories:
        category_name = category["name"]
        category_slug = category["slug"]

        print()
        print("=" * 80)
        print(f"Scraping category: {category_name} ({category_slug})")
        print("=" * 80)

        result = scrape_category(
            category_slug=category_slug,
            max_pages=None,
            count=48,
            client=client,
        )

        for announcement in result["data"]:
            unique_announcements[announcement["id"]] = announcement

        all_errors.extend(result["errors"])
        total_duplicates += result["duplicates"]

    all_announcements = list(unique_announcements.values())

    output = {
        "categories_count": len(categories),
        "total_announcements": len(all_announcements),
        "duplicates": total_duplicates,
        "errors": all_errors,
        "announcements": all_announcements,
    }

    with open(
        "output/all_categories.json",
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            output,
            file,
            ensure_ascii=False,
            indent=4,
        )

    print()
    print("=" * 80)
    print(f"Saved {len(all_announcements)} announcements")
    print(f"Categories processed: {len(categories)}")
    print(f"Duplicates skipped: {total_duplicates}")
    print(f"Errors: {len(all_errors)}")
    print("=" * 80)


def main():
    category_tree = fetch_category_tree()

    if not category_tree:
        raise RuntimeError("No categories returned by the Ouedkniss menu API.")

    mode = "interactive"

    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()

    if mode in {"quick", "test", "smoke"}:
        run_quick_test()
        return

    if mode in {"full", "all"}:
        run_full_mode()
        return

    if mode in {"interactive", "menu", "select"}:
        selected = select_category(category_tree)

        if selected == "all":
            run_full_mode()
            return

        if selected == "quick":
            run_quick_test()
            return

        run_single_category(selected, max_pages=1, count=5)
        return

    print("Unknown mode. Use: python main.py interactive | quick | full")


if __name__ == "__main__":
    main()