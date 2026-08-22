from .graphql.client import OuedknissClient


DETAILS_QUERY = """
query AnnouncementGet($id: ID!) {
    announcement: announcementDetails(id: $id) {
        id
        reference
        title
        slug
        description

        createdAt: refreshedAt

        price
        pricePreview
        oldPrice
        oldPricePreview
        priceType
        exchangeType
        priceUnit

        hasDelivery
        deliveryType
        hasPhone
        hasEmail

        status

        category {
            id
            slug
            name
            deliveryType

            parentTree {
                id
                name
                slug
            }
        }

        defaultMedia(size: ORIGINAL) {
            mediaUrl
            mimeType
            thumbnail
        }

        medias(size: LARGE) {
            mediaUrl
            mimeType
            thumbnail
        }

        categories {
            id
            name
            slug
            parentId
        }

        specs {
            specification {
                label
                codename
                type
            }
            value
            valueText
        }

        user {
            id
            username
            displayName
            avatarUrl
        }

        isFromStore

        store {
            id
            name
            slug
            imageUrl
            url
        }

        cities {
            id
            name

            region {
                id
                name
                slug
            }
        }

        variants {
            id
            hash

            specifications {
                specification {
                    codename
                    label
                }

                valueText
                value
                mediaUrl
            }

            price
            oldPrice
            pricePreview
            oldPricePreview
            quantity
        }
    }
}
"""


def get_announcement_details(announcement_id):
    client = OuedknissClient()

    result = client.execute(
        query=DETAILS_QUERY,
        variables={
            "id": str(announcement_id)
        },
        operation_name="AnnouncementGet"
    )

    return result["announcement"]