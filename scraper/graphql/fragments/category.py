CATEGORY_FRAGMENT = """
fragment CategoryContent on Category {
    id
    name
    slug
    icon
    delivery
    deliveryType
    isWithoutExchange
    priceUnits

    children {
        id
        name
        slug
        icon
        __typename
    }

    parentTree {
        id
        name
        slug
        icon

        children {
            id
            name
            slug
            icon
            __typename
        }

        __typename
    }

    parent {
        id
        name
        icon
        slug
        __typename
    }

    __typename
}
"""