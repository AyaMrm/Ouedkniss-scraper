
SEARCH_META_QUERY = """query SearchMetaQuery($q: String, $filter: SearchFilterInput) {
  search(q: $q, filter: $filter) {
    active {
      ...SearchActiveContent
      __typename
    }
    suggested {
      ...SearchSuggestedContent
      __typename
    }
    __typename
  }
}

fragment SearchActiveContent on SearchCategory {
  category {
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
    specifications {
      isRequired
      specification {
        id
        codename
        label
        type
        class
        datasets {
          codename
          label
          __typename
        }
        dependsOn {
          id
          codename
          __typename
        }
        subSpecifications {
          id
          codename
          label
          type
          __typename
        }
        allSubSpecificationCodenames
        __typename
      }
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
  count
  filter {
    cities {
      id
      name
      __typename
    }
    regions {
      id
      name
      __typename
    }
    __typename
  }
  __typename
}

fragment SearchSuggestedContent on SearchCategory {
  category {
    id
    name
    slug
    icon
    __typename
  }
  count
  __typename
}"""

SEARCH_ANNOUNCEMENTS_QUERY = """
query SearchAnnouncementsQuery($q: String, $filter: SearchFilterInput, $mediaSize: MediaSize = MEDIUM) {
  search(q: $q, filter: $filter) {
    announcements {
      ...SearchAnnouncementsContent
      __typename
    }
    __typename
  }
}

fragment SearchAnnouncementsContent on AnnouncementPagination {
  data {
    ...AnnouncementContentNoUserReaction
    smallDescription {
      specification {
        codename
        __typename
      }
      valueText
      __typename
    }
    noAdsense
    __typename
  }
  paginatorInfo {
    lastPage
    hasMorePages
    __typename
  }
  __typename
}

fragment AnnouncementContentNoUserReaction on Announcement {
  id
  title
  slug
  createdAt: refreshedAt
  isFromStore
  isCommentEnabled
  hasDelivery
  deliveryType
  paymentMethod
  likeCount
  description
  status
  cities {
    id
    name
    slug
    region {
      id
      name
      slug
      __typename
    }
    __typename
  }
  store {
    id
    name
    slug
    imageUrl
    isOfficial
    isVerified
    viewAsStore
    __typename
  }
  user {
    id
    __typename
  }
  defaultMedia(size: $mediaSize) {
    mediaUrl
    mimeType
    thumbnail
    __typename
  }
  medias(size: SMALL) {
    mediaUrl
    mimeType
    thumbnail
    __typename
  }
  price
  pricePreview
  priceUnit
  oldPrice
  oldPricePreview
  priceType
  exchangeType
  category {
    id
    slug
    deliveryType
    __typename
  }
  __typename
}
"""