def parse_specs(specs):
    result = {}

    for spec in specs:
        specification = spec.get("specification") or {}

        codename = specification.get("codename")
        values = spec.get("valueText") or []

        if not codename:
            continue

        if len(values) == 1:
            result[codename] = values[0]
        else:
            result[codename] = values

    return result


def parse_announcement(announcement):
    cities = announcement.get("cities") or []

    location = None

    if cities:
        city = cities[0]

        location = {
            "city": city.get("name"),
            "region": (city.get("region") or {}).get("name")
        }

    return {
        "id": announcement.get("id"),
        "title": announcement.get("title"),
        "description": announcement.get("description"),
        "price": announcement.get("price"),
        "price_unit": announcement.get("priceUnit"),

        "location": location,

        "category": announcement.get("category"),

        "specifications": parse_specs(
            announcement.get("specs") or []
        ),

        "images": [
            media.get("mediaUrl")
            for media in announcement.get("medias") or []
            if media.get("mediaUrl")
        ]
    }