import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from keepa_client import KeepaClient

app = FastAPI()

# CORS fix — whitelist your frontend URL or use "*" if you prefer open access
WEB_ORIGIN = os.environ.get("WEB_ORIGIN", "https://zentra-web.onrender.com")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[WEB_ORIGIN],   # or ["*"] if you want open CORS
    allow_credentials=True,       # only safe if not using "*" for allow_origins
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model for brand coverage
class CoverageRunReq(BaseModel):
    brand: str
    bsr_max: int = 250000
    require_buybox: bool = True
    max_pages: int = 3
    max_asins: int = 200

# Health endpoint
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
