"""
Category model for the finance tracker application.
"""
from typing import List, Optional


class Category:
    """
    Represents a category for classifying transactions.
    """
    def __init__(
        self,
        name: str,
        category_type: str = "expense",
        parent_category: Optional[str] = None,
        category_id: Optional[int] = None,
        budget_limit: Optional[float] = None,
    ):
        """
        Initialize a new Category.
        
        Args:
            name: The name of the category
            category_type: The type of the category ("expense" or "income")
            parent_category: Optional parent category for hierarchical categorization
            category_id: Unique identifier for the category (auto-assigned by storage)
            budget_limit: Optional monthly budget limit for this category
        """
        self.name = name
        if category_type not in ["expense", "income"]:
            raise ValueError("Category type must be 'expense' or 'income'")
        self.category_type = category_type
        self.parent_category = parent_category
        self.category_id = category_id
        self.budget_limit = budget_limit
    
    @property
    def is_expense_category(self) -> bool:
        """Return True if this is an expense category."""
        return self.category_type == "expense"
    
    @property
    def is_income_category(self) -> bool:
        """Return True if this is an income category."""
        return self.category_type == "income"
    
    @property
    def full_path(self) -> str:
        """Return the full hierarchical path of the category."""
        if self.parent_category:
            return f"{self.parent_category} > {self.name}"
        return self.name
    
    def to_dict(self) -> dict:
        """Convert category to dictionary for storage."""
        return {
            "name": self.name,
            "category_type": self.category_type,
            "parent_category": self.parent_category,
            "category_id": self.category_id,
            "budget_limit": self.budget_limit
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Category":
        """Create a Category object from dictionary data."""
        return cls(
            name=data["name"],
            category_type=data["category_type"],
            parent_category=data.get("parent_category"),
            category_id=data.get("category_id"),
            budget_limit=data.get("budget_limit")
        )
    
    def __repr__(self) -> str:
        """String representation of the category."""
        return f"Category: {self.full_path} ({self.category_type})"


# Default categories for initial setup
DEFAULT_EXPENSE_CATEGORIES = [
    "Housing",
    "Utilities",
    "Groceries",
    "Dining Out",
    "Transportation",
    "Healthcare",
    "Entertainment",
    "Shopping",
    "Education",
    "Personal Care",
    "Travel",
    "Gifts & Donations",
    "Insurance",
    "Investments",
    "Miscellaneous"
]

DEFAULT_INCOME_CATEGORIES = [
    "Salary",
    "Freelance",
    "Business",
    "Investments",
    "Gifts",
    "Other Income"
]


def create_default_categories() -> List[Category]:
    """Create and return a list of default categories."""
    categories = []
    
    # Create expense categories
    for name in DEFAULT_EXPENSE_CATEGORIES:
        categories.append(Category(name=name, category_type="expense"))
    
    # Create income categories
    for name in DEFAULT_INCOME_CATEGORIES:
        categories.append(Category(name=name, category_type="income"))
    
    return categories