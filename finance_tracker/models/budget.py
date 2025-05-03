"""
Budget model for the finance tracker application.
"""
from datetime import datetime
from decimal import Decimal
from typing import Optional, Dict, Union


class Budget:
    """
    Represents a budget for a specific time period.
    """
    def __init__(
        self,
        name: str,
        start_date: datetime,
        end_date: datetime,
        category_limits: Dict[str, Union[float, Decimal]],
        budget_id: Optional[int] = None,
        total_limit: Optional[Union[float, Decimal]] = None,
    ):
        """
        Initialize a new Budget.
        
        Args:
            name: The name of the budget
            start_date: When the budget period begins
            end_date: When the budget period ends
            category_limits: Dictionary mapping category names to budget limits
            budget_id: Unique identifier for the budget (auto-assigned by storage)
            total_limit: Optional overall spending limit for the budget period
        """
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        
        # Convert all amounts to Decimal for precise calculations
        self.category_limits = {
            category: Decimal(str(amount))
            for category, amount in category_limits.items()
        }
        
        self.budget_id = budget_id
        self.total_limit = Decimal(str(total_limit)) if total_limit else None
    
    @property
    def duration_days(self) -> int:
        """Return the duration of the budget in days."""
        delta = self.end_date - self.start_date
        return delta.days
    
    @property
    def is_active(self) -> bool:
        """Return True if the current date is within the budget period."""
        now = datetime.now()
        return self.start_date <= now <= self.end_date
    
    @property
    def total_category_limits(self) -> Decimal:
        """Return the sum of all category limits."""
        return sum(self.category_limits.values())
    
    def get_daily_limit(self, category: Optional[str] = None) -> Decimal:
        """
        Calculate the daily spending limit for a category or overall.
        
        Args:
            category: The category to get the limit for, or None for overall limit
        
        Returns:
            The daily spending limit as a Decimal
        """
        if category:
            if category not in self.category_limits:
                return Decimal('0')
            return self.category_limits[category] / self.duration_days
        
        # Return overall daily limit
        if self.total_limit:
            return self.total_limit / self.duration_days
        return self.total_category_limits / self.duration_days
    
    def to_dict(self) -> dict:
        """Convert budget to dictionary for storage."""
        return {
            "name": self.name,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat(),
            "category_limits": {
                category: str(amount)
                for category, amount in self.category_limits.items()
            },
            "budget_id": self.budget_id,
            "total_limit": str(self.total_limit) if self.total_limit else None,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Budget":
        """Create a Budget object from dictionary data."""
        return cls(
            name=data["name"],
            start_date=datetime.fromisoformat(data["start_date"]),
            end_date=datetime.fromisoformat(data["end_date"]),
            category_limits={
                category: Decimal(amount)
                for category, amount in data["category_limits"].items()
            },
            budget_id=data.get("budget_id"),
            total_limit=Decimal(data["total_limit"]) if data.get("total_limit") else None,
        )
    
    def __repr__(self) -> str:
        """String representation of the budget."""
        return (
            f"Budget: {self.name} "
            f"({self.start_date.strftime('%Y-%m-%d')} to {self.end_date.strftime('%Y-%m-%d')})"
        )