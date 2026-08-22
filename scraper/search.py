from .graphql.client import OuedknissClient


SEARCH_QUERY = """
query SearchAnnouncementsQuery(
    $q: String,
    $filter: SearchFilterInput,
    $mediaSize: MediaSize = MEDIUM
) {
    search(q: $q, filter: $filter) {
        announcements {
            data {
                id
                title
                slug
                createdAt: refreshedAt
                price
                pricePreview
                priceUnit
                oldPrice
                oldPricePreview
                priceType
                exchangeType

                cities {
                    id
                    name
                    slug
                    region {
                        id
                        name
                        slug
                    }
                }

                defaultMedia(size: $mediaSize) {
                    mediaUrl
                    mimeType
                    thumbnail
                }

                category {
                    id
                    slug
                    deliveryType
                }
            }

            paginatorInfo {
                lastPage
                hasMorePages
            }
        }
    }
}
"""


def search_announcements(category_slug, page=1, count=48):
    client = OuedknissClient()

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
        query=SEARCH_QUERY,
        variables=variables,
        operation_name="SearchAnnouncementsQuery"
    )