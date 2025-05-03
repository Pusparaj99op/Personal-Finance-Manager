"""
Transaction model for the finance tracker application.
"""
from datetime import datetime
from decimal import Decimal
from typing import Optional, Union


class Transaction:
    """
    Represents a financial transaction (expense or income).
    """
    def __init__(
        self,
        amount: Union[float, Decimal],
        category: str,
        description: str,
        transaction_date: Optional[datetime] = None,
        transaction_type: str = "expense",
        transaction_id: Optional[int] = None,
    ):
        """
        Initialize a new Transaction.
        
        Args:
            amount: The monetary amount of the transaction
            category: The category the transaction belongs to
            description: A brief description of the transaction
            transaction_date: When the transaction occurred (defaults to current time)
            transaction_type: Either "expense" or "income"
            transaction_id: Unique identifier for the transaction (auto-assigned by storage)
        """
        self.amount = Decimal(str(amount))  # Convert to Decimal for precise monetary calculations
        self.category = category
        self.description = description
        self.transaction_date = transaction_date or datetime.now()
        if transaction_type not in ["expense", "income"]:
            raise ValueError("Transaction type must be 'expense' or 'income'")
        self.transaction_type = transaction_type
        self.transaction_id = transaction_id
        
    @property
    def is_expense(self) -> bool:
        """Return True if this is an expense transaction."""
        return self.transaction_type == "expense"
    
    @property
    def is_income(self) -> bool:
        """Return True if this is an income transaction."""
        return self.transaction_type == "income"
    
    @property
    def signed_amount(self) -> Decimal:
        """Return the amount with a sign indicating expense (negative) or income (positive)."""
        if self.is_expense:
            return -abs(self.amount)
        return abs(self.amount)
    
    def to_dict(self) -> dict:
        """Convert transaction to dictionary for storage."""
        return {
            "amount": str(self.amount),
            "category": self.category,
            "description": self.description,
            "transaction_date": self.transaction_date.isoformat(),
            "transaction_type": self.transaction_type,
            "transaction_id": self.transaction_id,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Transaction":
        """Create a Transaction object from dictionary data."""
        return cls(
            amount=Decimal(data["amount"]),
            category=data["category"],
            description=data["description"],
            transaction_date=datetime.fromisoformat(data["transaction_date"]),
            transaction_type=data["transaction_type"],
            transaction_id=data.get("transaction_id"),
        )
    
    def __repr__(self) -> str:
        """String representation of the transaction."""
        return (
            f"{self.transaction_type.capitalize()}: {self.amount} "
            f"({self.category}) - {self.description} "
            f"on {self.transaction_date.strftime('%Y-%m-%d')}"
        )