from .graphql.client import OuedknissClient
from .graphql.queries.menu import LISTING_MENU_QUERY


def _normalize_category(target):
    if not target:
        return None

    is_category = target.get("__typename") == "Category" or all(
        key in target for key in ("id", "name", "slug")
    )

    if not is_category:
        return None

    children = target.get("children") or []
    normalized_children = []

    for child in children:
        normalized = _normalize_category(child)
        if normalized is not None:
            normalized_children.append(normalized)

    return {
        "id": target.get("id"),
        "name": target.get("name"),
        "slug": target.get("slug"),
        "children": normalized_children,
    }


def fetch_categories():
    """
    Fetch the flat list of available categories from the Ouedkniss menu.
    """
    category_tree = fetch_category_tree()

    flat_categories = []

    def walk(node):
        flat_categories.append({
            "id": node["id"],
            "name": node["name"],
            "slug": node["slug"],
        })

        for child in node.get("children", []):
            walk(child)

    for node in category_tree:
        walk(node)

    return flat_categories


def fetch_category_tree():
    """
    Fetch the categories as a hierarchical tree from the Ouedkniss menu.
    """
    client = OuedknissClient()

    response = client.execute(
        query=LISTING_MENU_QUERY,
        variables={"menuFilter": None},
        operation_name="listingMenu"
    )

    category_tree = []

    for item in response.get("listingMenu", []):
        category = _normalize_category(item.get("target"))
        if category is not None:
            category_tree.append(category)

    return category_tree
