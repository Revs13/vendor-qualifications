# Vendor Qualifications Project

## Overview

The goal of this project was to develop a system to rank software vendors based on feature similarity and vendor ratings. Given a CSV of software vendors with their categories, features, and ratings, the objective was to allow a user to search for vendors matching specific capabilities and return a ranked list.

> ⚠️ Note: This project is a prototype and may not fully handle all datasets or edge cases yet. It demonstrates the approach taken, the steps implemented, and potential improvements that could make the system fully functional.

---
**Intended functionality:**

- Load a CSV of software vendors including their category, features, and ratings.
- Allow users to search for vendors by category and capabilities.
- Compute feature similarity scores and rank vendors accordingly.
- Combine feature similarity and vendor rating to calculate a final score.

> ⚠️ Note: This project is a prototype and may not fully handle all datasets or edge cases yet.

## Key Features Implemented

- CSV ingestion and preprocessing for key columns: `product_name`, `main_category`, `Features`, `rating`.
- TF-IDF vectorization of vendor features and category for similarity computation.
- Vendor ranking based on a combination of similarity and normalized rating.
- JSON-safe output for potential API integration.

---

## Description of Steps Taken

1. **Data Processing & Ingestion**
   - Loaded the sample CSV file of software vendors.
   - Preprocessed key columns: 
     - `product_name` (software name)
     - `main_category` (e.g., CRM, ERP, Accounting & Finance Software)
     - `Features` (capabilities)
     - `rating` (vendor rating)
   - Filled missing values and normalized text (lowercasing, removing NaNs).

2. **Feature Vectorization**
   - Combined `Features` and `main_category` into a single text column.
   - Used **TF-IDF vectorization** to represent vendors as numerical vectors for similarity comparison.
   - Chose n-grams `(1,2)` to capture multi-word features like “email marketing”.

3. **Capability Matching & Similarity Scoring**
   - Constructed a query vector from user-provided capabilities.
   - Computed cosine similarity between vendor vectors and the query.
   - Planned to filter vendors based on a threshold (e.g., ≥ 0.6), ensuring only relevant vendors were returned.

4. **Ranking Vendors**
   - Intended to rank vendors using a **weighted combination of feature similarity and normalized rating**.
   - Also considered incorporating the number of reviews for additional weighting.

---

## Challenges Encountered

- Persistent **server errors** when testing with FastAPI prevented full API implementation.
- Some CSV fields contain **nested JSON-like structures**, making parsing and feature extraction more complex.
- Limited time for completion made it difficult to fully implement multi-feature weighting and final ranking.

---

## Potential Improvements / Next Steps

1. **Robust Feature Parsing**
   - Properly parse JSON-like columns such as `pros_list` and `cons_list`.
   - Extract individual features from nested structures.

2. **Improved Vendor Ranking**
   - Weight vendors based on multiple feature matches.
   - Incorporate additional vendor metadata such as review count, social media presence, or total revenue.

3. **API Integration**
   - Implement a FastAPI endpoint for real-time search and ranking.
   - Include error handling and JSON-safe output.

4. **Scalability & Performance**
   - Optimize TF-IDF computation for large datasets.
   - Handle edge cases and missing data more gracefully.

---
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

## How to Use (Prototype)

```python
from vendor_ranker import VendorRanker

# Initialize the class with your CSV
ranker = VendorRanker("G2_software.csv")

# Search for vendors in a specific category with desired capabilities
results = ranker.search_rank(
    software_category="CRM",
    capabilities=["email marketing", "automation"],
    top_k=5
)

for r in results:
    print(r)
