from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from .vendor_ranker import VendorRanker

app = FastAPI(title="Vendor Qualification API")

# Initialize ranker once
ranker = VendorRanker("data/vendors.csv")

class RankRequest(BaseModel):
    software_category: str
    capabilities: List[str]
    top_k: int = 10
    threshold: float = 0.6

@app.post("/rank")
def rank_vendors(req: RankRequest):
    results = ranker.search_rank(
        software_category=req.software_category,
        capabilities=req.capabilities,
        top_k=req.top_k,
        threshold=req.threshold
    )
    return {"results": results}
