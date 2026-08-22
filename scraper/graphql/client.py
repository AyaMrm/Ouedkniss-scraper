import requests


class OuedknissClient:
    BASE_URL = "https://api.ouedkniss.com/graphql"

    def __init__(self):
        self.session = requests.Session()

        self.session.headers.update({
            "Accept": "*/*",
            "Content-Type": "application/json",
            "Accept-Language": "fr",
            "Locale": "fr",
            "Origin": "https://www.ouedkniss.com",
            "Referer": "https://www.ouedkniss.com/",
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/151.0.0.0 Safari/537.36"
            ),
            "X-App-Version": "3.6.17",
        })

    def execute(self, query, variables=None, operation_name=None):
        payload = {
            "operationName": operation_name,
            "variables": variables or {},
            "query": query,
        }

        response = self.session.post(
            self.BASE_URL,
            json=payload,
            timeout=30,
        )

        response.raise_for_status()

        data = response.json()

        if "errors" in data:
            raise RuntimeError(data["errors"])

        return data["data"]
