# Vendor Qualifications

Python project to rank software vendors based on feature similarity and vendor ratings.

## Overview

The `VendorRanker` project is designed to help users discover and rank software vendors by matching desired capabilities (features) with vendor-provided feature lists. The project uses TF-IDF vectorization and cosine similarity to compare user queries against vendor features and produces a ranked list of vendors.

**Intended functionality:**

- Load a CSV of software vendors including their category, features, and ratings.
- Allow users to search for vendors by category and capabilities.
- Compute feature similarity scores and rank vendors accordingly.
- Combine feature similarity and vendor rating to calculate a final score.

> ⚠️ Note: This project is a prototype and may not fully handle all datasets or edge cases yet.

## Features Implemented

- CSV ingestion and preprocessing for key columns: `product_name`, `main_category`, `Features`, `rating`.
- TF-IDF vectorization of vendor features and category for similarity computation.
- Vendor ranking based on a combination of similarity and normalized rating.
- JSON-safe output for potential API integration.

## Repository Structure
- requirements.txt - Contains all requirements necessary to run this code.
- data 
   |
    - vendors.csv - The CSV file containing vendor information like name, category, and features/capabilities.
- app
   |
    - main.py - Dictates which ranker functions are called based on API endpoint.
   |
    - vendor_ranker.py - Contains functions for ranking input CSV of vendors.

## How to Use

```python
from vendor_ranker import VendorRanker

ranker = VendorRanker("G2_software.csv")
results = ranker.search_rank(
    software_category="CRM",
    capabilities=["email marketing", "automation"],
    top_k=5
)
for r in results:
    print(r)
