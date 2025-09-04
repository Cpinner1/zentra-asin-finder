import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from keepa_client import KeepaClient

app = FastAPI()

# CORS fix: Open CORS without credentials so browsers accept it
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # Allow all origins for testing
    allow_credentials=False,    # Must be False with "*"
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request body model
class CoverageRunReq(BaseModel):
    brand: str
    bsr_max: int = 250000
    require_buybox: bool = True
    max_pages: int = 3
    max_asins: int = 200

# Health check
@app.get("/health")
def health():
    return {"ok": True}

# Brand coverage endpoint
@app.post("/brands/coverage")
def brand_coverage(req: CoverageRunReq):
    key = os.environ.get("KEEPA_KEY")
    if not key:
        raise HTTPException(500, "Missing KEEPA_KEY environment variable")

    domain = int(os.environ.get("KEEPA_DOMAIN", "1"))
    kc = KeepaClient(key, domain)

    selection = {
        "brand": req.brand,
        "isActive": True,
        "current_SalesRankRange": [1, req.bsr_max],
    }
    if req.require_buybox:
        selection["hasBuyBox"] = True

    page = 0
    asins = set()

    while True:
        data = kc.finder(selection, page)
        products = data.get("products") or []
        if not products:
            break

        for p in products:
            asin = (p.get("asin") or "").upper()
            if asin:
                asins.add(asin)
                if len(asins) >= req.max_asins:
                    break

        if len(asins) >= req.max_asins or page >= req.max_pages:
            break

        page += 1

    return {
        "brand": req.brand,
        "count": len(asins),
        "asins": sorted(asins)[: req.max_asins],
    }
