LISTING_MENU_QUERY = """
query listingMenu($menuFilter: MenuFilterInput) {
  listingMenu: menuFetch(menuFilter: $menuFilter) {
    id
    name
    icon {
      light
      dark
      __typename
    }
    target {
      __typename
      ... on Category {
        id
        name
        slug
        icon
        active
        rank
        delivery
        deliveryType
        isWithoutExchange
        priceUnits
        children {
          id
          name
          slug
          icon
          active
          rank
          __typename
        }
        parent {
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
          __typename
        }
        __typename
      }
    }
    rank
    __typename
  }
}
"""
