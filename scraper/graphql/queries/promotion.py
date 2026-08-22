PROMOTION_SLIDER_QUERY="""query PromoSliderQuery($location: PromotionLocation!, $count: Int, $categoryId: ID, $categorySlug: String) {
  list: promotionFetch(
    location: $location
    maxCount: $count
    categoryId: $categoryId
    categorySlug: $categorySlug
  ) {
    id
    name
    targetLink
    targetType
    targetId
    currentVisual {
      targetLink
      media {
        mediaUrl: media
        mimeType
        __typename
      }
      mediaMobile {
        mediaUrl: media
        mimeType
        __typename
      }
      __typename
    }
    __typename
  }
}"""
