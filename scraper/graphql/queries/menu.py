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
        __typename
      }
    }
    rank
    __typename
  }
}
"""
