ANNOUNCEMENT_FRAGMENT = """
fragment AnnouncementContent on Announcement {
    id
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

    status
    quantity

    hasDelivery
    deliveryType
    hasPhone
    hasEmail

    isFromStore
    isCommentEnabled

    __typename
}
"""