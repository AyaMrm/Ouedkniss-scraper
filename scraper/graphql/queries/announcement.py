ANNOUNCEMENT_DETAILS_QUERY = """query AnnouncementGet($id: ID!) {
  announcement: announcementDetails(id: $id) {
    id
    reference
    title
    slug
    description
    orderExternalUrl
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
    quantity
    status
    street_name
    category {
      id
      slug
      name
      deliveryType
      parentTree {
        id
        name
        slug
        __typename
      }
      __typename
    }
    defaultMedia(size: ORIGINAL) {
      mediaUrl
      mimeType
      thumbnail
      __typename
    }
    medias(size: LARGE) {
      mediaUrl
      mimeType
      thumbnail
      __typename
    }
    categories {
      id
      name
      slug
      parentId
      __typename
    }
    specs {
      specification {
        label
        codename
        type
        __typename
      }
      value
      valueText
      __typename
    }
    user {
      id
      username
      displayName
      avatarUrl
      __typename
    }
    isFromStore
    store {
      id
      name
      slug
      description
      imageUrl
      url
      followerCount
      viewAsStore
      metaPixelId
      announcementsCount
      status
      locations {
        location {
          address
          region {
            slug
            name
            __typename
          }
          __typename
        }
        __typename
      }
      categories {
        name
        slug
        __typename
      }
      __typename
    }
    cities {
      id
      name
      region {
        id
        name
        slug
        __typename
      }
      __typename
    }
    isCommentEnabled
    noAdsense
    variants {
      id
      hash
      specifications {
        specification {
          codename
          label
          __typename
        }
        valueText
        value
        mediaUrl
        __typename
      }
      price
      oldPrice
      pricePreview
      oldPricePreview
      quantity
      __typename
    }
    showAnalytics
    messengerLink
    __typename
  }
}"""
