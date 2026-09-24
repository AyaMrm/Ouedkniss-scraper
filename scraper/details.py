from .graphql.client import OuedknissClient
from .graphql.queries.announcement import ANNOUNCEMENT_DETAILS_QUERY


def get_announcement_details(announcement_id, client=None):
    client = client or OuedknissClient()

    result = client.execute(
        query=DETAILS_QUERY,
        variables={
            "id": str(announcement_id)
        },
        operation_name="AnnouncementGet"
    )

    return result["announcement"]