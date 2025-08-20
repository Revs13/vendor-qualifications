import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

class VendorRanker:
    def __init__(self, csv_path="data/vendors.csv"):
        # Load CSV
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"CSV not found at {csv_path}")
        self.df = pd.read_csv(csv_path)

        # Ensure important columns exist
        required = ["product_name", "main_category", "Features"]
        for col in required:
            if col not in self.df.columns:
                raise ValueError(f"Missing required column: {col}")

        # Normalize text
        self.df["product_name"] = self.df["product_name"].fillna("").str.lower()
        self.df["main_category"] = self.df["main_category"].fillna("").str.lower()
        self.df["Features"] = self.df["Features"].fillna("").str.lower()

        # Ratings
        if "rating" in self.df.columns:
            self.df["rating"] = pd.to_numeric(self.df["rating"], errors="coerce").fillna(0.0)
        else:
            self.df["rating"] = 0.0

        # Vectorize features
        self.vectorizer = TfidfVectorizer()
        self.feature_matrix = self.vectorizer.fit_transform(self.df["Features"])

    def search_rank(self, software_category: str, capabilities: list, top_k: int = 10, threshold: float = 0.6):
        """Rank vendors by category + requested capabilities."""
        category = software_category.lower()
        capabilities = [c.lower() for c in capabilities]

        # Filter vendors by category
        subset = self.df[self.df["main_category"].str.lower().str.strip().str.contains(category, regex=False, na=False)]
        if subset.empty:
            return []

        # Build query vector
        query_text = " ".join(capabilities)
        query_vec = self.vectorizer.transform([query_text])

        # Calculate cosine similarity
        #subset_idx = subset.index
        subset_feature_matrix = self.vectorizer.transform(subset["Features"])
        sims = cosine_similarity(subset_feature_matrix, query_vec).flatten()


        # Add similarity scores
        subset = subset.copy()
        subset["similarity"] = sims
        # Combine similarity + rating first
        subset["final_score"] = 0.7 * subset["similarity"] + 0.3 * (subset["rating"] / 5.0)
        # Then sort
        subset = subset.sort_values(by="final_score", ascending=False).head(top_k)


        if subset.empty:
            return []

        # Combine similarity + rating
        subset["final_score"] = 0.7 * subset["similarity"] + 0.3 * (subset["rating"] / 5.0)

        # Sort by final score
        subset = subset.sort_values(by="final_score", ascending=False).head(top_k)

        return subset[[
            "product_name",
            "main_category",
            "similarity",
            "rating",
            "final_score",
            "Features"
        ]].to_dict(orient="records")








import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

class VendorRanker:
    def __init__(self, csv_path: str):
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"CSV not found at {csv_path}")
        
        # Load CSV safely
        self.df = pd.read_csv(csv_path, dtype=str, quoting=2)  # read everything as string

        # Ensure required columns exist
        for col in ["product_name", "main_category", "Features", "rating"]:
            if col not in self.df.columns:
                self.df[col] = ""

        # Fill missing values & lowercase
        for col in ["product_name", "main_category", "Features"]:
            self.df[col] = self.df[col].fillna("").str.lower()

        # Numeric rating
        self.df["rating"] = pd.to_numeric(self.df["rating"], errors="coerce").fillna(0.0)

        # Combine Features with main_category for vectorization
        self.df["combined_text"] = self.df["Features"] + " " + self.df["main_category"]

        # Precompute TF-IDF for the dataset
        self.vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1,2))
        self.feature_matrix = self.vectorizer.fit_transform(self.df["combined_text"])

    def search_rank(self, software_category: str, capabilities: list, top_k: int = 10, threshold: float = 0.6):
        """
        - software_category: e.g., "CRM"
        - capabilities: list of capabilities to match e.g., ["budgeting"]
        - threshold: similarity threshold for including vendors
        """
        # Normalize input
        category = software_category.lower()
        capabilities = [c.lower() for c in capabilities]

        # Filter vendors by category
        subset = self.df[self.df["main_category"].str.contains(category, na=False)]
        if subset.empty:
            return []

        # Precompute subset TF-IDF matrix
        subset_idx = subset.index.tolist()
        subset_matrix = self.feature_matrix[subset_idx]

        # Build query vector for all capabilities combined
        query_text = " ".join(capabilities)
        query_vec = self.vectorizer.transform([query_text])

        # Compute cosine similarity
        sims = cosine_similarity(subset_matrix, query_vec).flatten()

        # Filter by threshold (e.g., >= 0.6)
        subset = subset.copy()
        subset["similarity"] = sims
        subset = subset[subset["similarity"] >= threshold]
        if subset.empty:
            return []

        # Rank vendors: weighted final score
        # 70% similarity + 30% rating (normalized 0-1)
        subset["final_score"] = 0.7 * subset["similarity"] + 0.3 * (subset["rating"] / 5.0)

        # Sort by final_score descending and select top_k
        subset = subset.sort_values(by="final_score", ascending=False).head(top_k)

        # Return JSON-serializable dict
        result = subset[[
            "product_name", "main_category", "Features", "similarity", "rating", "final_score"
        ]].copy()
        for col in result.columns:
            result[col] = result[col].astype(str)

        return result.to_dict(orient="records")
