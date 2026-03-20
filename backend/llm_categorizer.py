import random

class LLMCategorizer:
    def __init__(self):
        self.categories = ["Food", "Rent", "Bills", "Shopping", "Miscellaneous", "Utilities"]

    def categorize(self, merchant: str, description: str) -> str:
        """
        Placeholder for LLM-based categorization.
        In a real scenario, this would call an LLM API.
        For now, it returns a random category.
        """
        # Simple rule-based categorization for demonstration
        if "starbucks" in merchant.lower() or "cafe" in description.lower():
            return "Food"
        elif "landlord" in merchant.lower() or "rent" in description.lower():
            return "Rent"
        elif "electricity" in description.lower() or "water" in description.lower():
            return "Utilities"
        elif "amazon" in merchant.lower() or "store" in description.lower():
            return "Shopping"
        elif "bill" in description.lower():
            return "Bills"
        else:
            return random.choice(self.categories)

