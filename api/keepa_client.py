import json, time, httpx

class KeepaClient:
    def __init__(self, key: str, domain: int = 1):
        self.key = key
        self.domain = domain
        self.http = httpx.Client(timeout=45)

    def finder(self, selection: dict, page: int = 0):
        r = self.http.get(
            "https://api.keepa.com/query",
            params={
                "key": self.key,
                "domain": self.domain,
                "selection": json.dumps(selection),
                "page": page,
            },
        )
        data = r.json()
        if data.get("tokensLeft", 1) <= 0 and data.get("refillIn", 0) > 0:
            time.sleep(data["refillIn"]/1000 + 0.5)
            return self.finder(selection, page)
        return data
