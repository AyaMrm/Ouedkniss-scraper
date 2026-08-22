import time

from .details import get_announcement_details
from .parser import parse_announcement


MAX_RETRIES = 3
RETRY_DELAY = 2


def fetch_details_with_retry(announcement_id):
    for attempt in range(1, MAX_RETRIES + 1):

        try:
            details = get_announcement_details(announcement_id)

            if not details:
                raise ValueError("Empty response")

            return details

        except Exception as error:

            print(
                f"! Error for {announcement_id} "
                f"(attempt {attempt}/{MAX_RETRIES}): {error}"
            )

            if attempt < MAX_RETRIES:
                time.sleep(RETRY_DELAY)

    print(
        f"! Failed permanently: {announcement_id}"
    )

    return None


def scrape_page(category_slug, page=1, count=48):

    from .search import search_announcements

    result = search_announcements(
        category_slug=category_slug,
        page=page,
        count=count
    )

    announcements = result["search"]["announcements"]

    parsed_announcements = []
    errors = []

    total = len(announcements["data"])

    for index, announcement in enumerate(
        announcements["data"],
        start=1
    ):

        announcement_id = announcement["id"]

        print(
            f"[{index}/{total}] "
            f"Fetching {announcement_id}..."
        )

        details = fetch_details_with_retry(
            announcement_id
        )

        if details is None:

            errors.append(announcement_id)

            continue

        try:

            parsed = parse_announcement(details)

            parsed_announcements.append(parsed)

        except Exception as error:

            print(
                f"! Parser error for "
                f"{announcement_id}: {error}"
            )

            errors.append(announcement_id)

    return {
        "data": parsed_announcements,
        "pagination": announcements["paginatorInfo"],
        "errors": errors
    }
    
def scrape_category(category_slug, max_pages=3, count=48):

    unique_announcements = {}
    all_errors = []
    duplicates = 0

    for page in range(1, max_pages + 1):

        print()
        print("=" * 50)
        print(f"PAGE {page}/{max_pages}")
        print("=" * 50)

        try:
            result = scrape_page(
                category_slug=category_slug,
                page=page,
                count=count
            )

        except Exception as error:
            print(f"✗ Error on page {page}: {error}")
            continue

        for announcement in result["data"]:
            announcement_id = announcement["id"]

            if announcement_id in unique_announcements:
                duplicates += 1
                continue

            unique_announcements[announcement_id] = announcement

        all_errors.extend(result["errors"])

        pagination = result["pagination"]

        print(
            f"Page {page}: "
            f"{len(result['data'])} annonces récupérées"
        )

        if not pagination["hasMorePages"]:
            print("✓ Dernière page atteinte.")
            break

    return {
        "data": list(unique_announcements.values()),
        "errors": all_errors,
        "duplicates": duplicates,
    }