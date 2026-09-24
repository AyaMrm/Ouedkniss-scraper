from .graphql.client import OuedknissClient
from .graphql.queries.search import SEARCH_ANNOUNCEMENTS_QUERY


def search_announcements(category_slug, page=1, count=48, client=None):
    client = client or OuedknissClient()

    variables = {
        "q": None,
        "filter": {
            "categorySlug": category_slug,
            "origin": None,
            "connected": False,
            "delivery": None,
            "regionIds": [],
            "cityIds": [],
            "priceRange": [],
            "exchange": None,
            "hasPictures": False,
            "hasPrice": False,
            "priceUnit": None,
            "fields": [],
            "page": page,
            "orderByField": {
                "field": "REFRESHED_AT"
            },
            "count": count
        }
    }

    return client.execute(
        query=SEARCH_ANNOUNCEMENTS_QUERY,
        variables=variables,
        operation_name="SearchAnnouncementsQuery"
    )