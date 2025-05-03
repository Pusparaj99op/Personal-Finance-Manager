"""
Unit tests for the finance tracker data models.
"""
import unittest
from datetime import datetime, timedelta
from decimal import Decimal

from finance_tracker.models.transaction import Transaction
from finance_tracker.models.category import Category, create_default_categories
from finance_tracker.models.budget import Budget


class TestTransaction(unittest.TestCase):
    """Tests for the Transaction class."""
    
    def test_transaction_creation(self):
        """Test creating a transaction."""
        tx = Transaction(
            amount=100.50,
            category="Groceries",
            description="Weekly grocery shopping",
            transaction_date=datetime(2025, 5, 1),
            transaction_type="expense"
        )
        
        self.assertEqual(tx.amount, Decimal('100.50'))
        self.assertEqual(tx.category, "Groceries")
        self.assertEqual(tx.description, "Weekly grocery shopping")
        self.assertEqual(tx.transaction_date, datetime(2025, 5, 1))
        self.assertEqual(tx.transaction_type, "expense")
        self.assertIsNone(tx.transaction_id)
    
    def test_transaction_is_expense(self):
        """Test is_expense property."""
        expense = Transaction(100, "Food", "Lunch", transaction_type="expense")
        income = Transaction(500, "Salary", "Monthly payment", transaction_type="income")
        
        self.assertTrue(expense.is_expense)
        self.assertFalse(income.is_expense)
    
    def test_transaction_is_income(self):
        """Test is_income property."""
        expense = Transaction(100, "Food", "Lunch", transaction_type="expense")
        income = Transaction(500, "Salary", "Monthly payment", transaction_type="income")
        
        self.assertFalse(expense.is_income)
        self.assertTrue(income.is_income)
    
    def test_signed_amount(self):
        """Test signed_amount property."""
        expense = Transaction(100, "Food", "Lunch", transaction_type="expense")
        income = Transaction(500, "Salary", "Monthly payment", transaction_type="income")
        
        self.assertEqual(expense.signed_amount, Decimal('-100'))
        self.assertEqual(income.signed_amount, Decimal('500'))
    
    def test_to_dict(self):
        """Test conversion to dictionary."""
        tx_date = datetime.now()
        tx = Transaction(
            amount=75.25,
            category="Entertainment",
            description="Movie tickets",
            transaction_date=tx_date,
            transaction_type="expense",
            transaction_id=42
        )
        
        tx_dict = tx.to_dict()
        
        self.assertEqual(tx_dict["amount"], "75.25")
        self.assertEqual(tx_dict["category"], "Entertainment")
        self.assertEqual(tx_dict["description"], "Movie tickets")
        self.assertEqual(tx_dict["transaction_date"], tx_date.isoformat())
        self.assertEqual(tx_dict["transaction_type"], "expense")
        self.assertEqual(tx_dict["transaction_id"], 42)
    
    def test_from_dict(self):
        """Test creating transaction from dictionary."""
        tx_date = datetime.now()
        tx_dict = {
            "amount": "42.42",
            "category": "Bills",
            "description": "Electricity",
            "transaction_date": tx_date.isoformat(),
            "transaction_type": "expense",
            "transaction_id": 123
        }
        
        tx = Transaction.from_dict(tx_dict)
        
        self.assertEqual(tx.amount, Decimal('42.42'))
        self.assertEqual(tx.category, "Bills")
        self.assertEqual(tx.description, "Electricity")
        self.assertEqual(tx.transaction_date.isoformat(), tx_date.isoformat())
        self.assertEqual(tx.transaction_type, "expense")
        self.assertEqual(tx.transaction_id, 123)
    
    def test_invalid_transaction_type(self):
        """Test validation of transaction type."""
        with self.assertRaises(ValueError):
            Transaction(100, "Food", "Lunch", transaction_type="invalid")


class TestCategory(unittest.TestCase):
    """Tests for the Category class."""
    
    def test_category_creation(self):
        """Test creating a category."""
        cat = Category(
            name="Groceries",
            category_type="expense",
            parent_category="Food",
            budget_limit=300
        )
        
        self.assertEqual(cat.name, "Groceries")
        self.assertEqual(cat.category_type, "expense")
        self.assertEqual(cat.parent_category, "Food")
        self.assertEqual(cat.budget_limit, 300)
        self.assertIsNone(cat.category_id)
    
    def test_is_expense_category(self):
        """Test is_expense_category property."""
        expense_cat = Category("Dining", "expense")
        income_cat = Category("Salary", "income")
        
        self.assertTrue(expense_cat.is_expense_category)
        self.assertFalse(income_cat.is_expense_category)
    
    def test_is_income_category(self):
        """Test is_income_category property."""
        expense_cat = Category("Dining", "expense")
        income_cat = Category("Salary", "income")
        
        self.assertFalse(expense_cat.is_income_category)
        self.assertTrue(income_cat.is_income_category)
    
    def test_full_path(self):
        """Test full_path property."""
        cat1 = Category("Groceries", "expense")
        cat2 = Category("Organic", "expense", parent_category="Groceries")
        
        self.assertEqual(cat1.full_path, "Groceries")
        self.assertEqual(cat2.full_path, "Groceries > Organic")
    
    def test_to_dict(self):
        """Test conversion to dictionary."""
        cat = Category(
            name="Entertainment",
            category_type="expense",
            parent_category="Discretionary",
            category_id=5,
            budget_limit=150
        )
        
        cat_dict = cat.to_dict()
        
        self.assertEqual(cat_dict["name"], "Entertainment")
        self.assertEqual(cat_dict["category_type"], "expense")
        self.assertEqual(cat_dict["parent_category"], "Discretionary")
        self.assertEqual(cat_dict["category_id"], 5)
        self.assertEqual(cat_dict["budget_limit"], 150)
    
    def test_from_dict(self):
        """Test creating category from dictionary."""
        cat_dict = {
            "name": "Rent",
            "category_type": "expense",
            "parent_category": "Housing",
            "category_id": 10,
            "budget_limit": 1200
        }
        
        cat = Category.from_dict(cat_dict)
        
        self.assertEqual(cat.name, "Rent")
        self.assertEqual(cat.category_type, "expense")
        self.assertEqual(cat.parent_category, "Housing")
        self.assertEqual(cat.category_id, 10)
        self.assertEqual(cat.budget_limit, 1200)
    
    def test_invalid_category_type(self):
        """Test validation of category type."""
        with self.assertRaises(ValueError):
            Category("Invalid", "not_a_valid_type")
    
    def test_default_categories(self):
        """Test creation of default categories."""
        categories = create_default_categories()
        
        # Check that we have the expected number of categories
        self.assertTrue(len(categories) > 0)
        
        # Check that categories have the expected types
        expense_cats = [c for c in categories if c.category_type == "expense"]
        income_cats = [c for c in categories if c.category_type == "income"]
        
        self.assertTrue(len(expense_cats) > 0)
        self.assertTrue(len(income_cats) > 0)


class TestBudget(unittest.TestCase):
    """Tests for the Budget class."""
    
    def test_budget_creation(self):
        """Test creating a budget."""
        start_date = datetime(2025, 5, 1)
        end_date = datetime(2025, 5, 31)
        category_limits = {
            "Groceries": 400,
            "Dining": 200,
            "Entertainment": 150
        }
        
        budget = Budget(
            name="May 2025",
            start_date=start_date,
            end_date=end_date,
            category_limits=category_limits,
            budget_id=1,
            total_limit=1500
        )
        
        self.assertEqual(budget.name, "May 2025")
        self.assertEqual(budget.start_date, start_date)
        self.assertEqual(budget.end_date, end_date)
        self.assertEqual(budget.budget_id, 1)
        self.assertEqual(budget.total_limit, Decimal('1500'))
        
        # Check category limits are converted to Decimal
        self.assertEqual(budget.category_limits["Groceries"], Decimal('400'))
        self.assertEqual(budget.category_limits["Dining"], Decimal('200'))
        self.assertEqual(budget.category_limits["Entertainment"], Decimal('150'))
    
    def test_duration_days(self):
        """Test duration_days property."""
        start_date = datetime(2025, 5, 1)
        end_date = datetime(2025, 5, 31)
        
        budget = Budget(
            name="May 2025",
            start_date=start_date,
            end_date=end_date,
            category_limits={}
        )
        
        self.assertEqual(budget.duration_days, 30)
    
    def test_is_active(self):
        """Test is_active property."""
        now = datetime.now()
        past_start = now - timedelta(days=10)
        future_end = now + timedelta(days=10)
        past_end = now - timedelta(days=5)
        future_start = now + timedelta(days=5)
        
        # Active budget (current date is within the budget period)
        active_budget = Budget(
            name="Active",
            start_date=past_start,
            end_date=future_end,
            category_limits={}
        )
        
        # Past budget (already ended)
        past_budget = Budget(
            name="Past",
            start_date=past_start,
            end_date=past_end,
            category_limits={}
        )
        
        # Future budget (not started yet)
        future_budget = Budget(
            name="Future",
            start_date=future_start,
            end_date=future_end,
            category_limits={}
        )
        
        self.assertTrue(active_budget.is_active)
        self.assertFalse(past_budget.is_active)
        self.assertFalse(future_budget.is_active)
    
    def test_total_category_limits(self):
        """Test total_category_limits property."""
        category_limits = {
            "Groceries": 400,
            "Dining": 200,
            "Entertainment": 150
        }
        
        budget = Budget(
            name="Test Budget",
            start_date=datetime(2025, 5, 1),
            end_date=datetime(2025, 5, 31),
            category_limits=category_limits
        )
        
        self.assertEqual(budget.total_category_limits, Decimal('750'))
    
    def test_get_daily_limit(self):
        """Test get_daily_limit method."""
        start_date = datetime(2025, 5, 1)
        end_date = datetime(2025, 5, 31)  # 31 days
        category_limits = {
            "Groceries": Decimal('310'),  # 10 per day
            "Dining": Decimal('155'),     # 5 per day
            "Entertainment": Decimal('93') # 3 per day
        }
        
        budget = Budget(
            name="May 2025",
            start_date=start_date,
            end_date=end_date,
            category_limits=category_limits,
            total_limit=Decimal('1000')  # ~32.26 per day
        )
        
        # Test daily limit for specific categories
        self.assertAlmostEqual(float(budget.get_daily_limit("Groceries")), 10.0, places=2)
        self.assertAlmostEqual(float(budget.get_daily_limit("Dining")), 5.0, places=2)
        self.assertAlmostEqual(float(budget.get_daily_limit("Entertainment")), 3.0, places=2)
        
        # Test category that doesn't exist
        self.assertEqual(budget.get_daily_limit("NonExistent"), Decimal('0'))
        
        # Test overall daily limit
        self.assertAlmostEqual(float(budget.get_daily_limit()), 32.26, places=2)
    
    def test_to_dict(self):
        """Test conversion to dictionary."""
        start_date = datetime(2025, 5, 1)
        end_date = datetime(2025, 5, 31)
        category_limits = {
            "Groceries": Decimal('400'),
            "Dining": Decimal('200')
        }
        
        budget = Budget(
            name="May 2025",
            start_date=start_date,
            end_date=end_date,
            category_limits=category_limits,
            budget_id=1,
            total_limit=Decimal('1500')
        )
        
        budget_dict = budget.to_dict()
        
        self.assertEqual(budget_dict["name"], "May 2025")
        self.assertEqual(budget_dict["start_date"], start_date.isoformat())
        self.assertEqual(budget_dict["end_date"], end_date.isoformat())
        self.assertEqual(budget_dict["budget_id"], 1)
        self.assertEqual(budget_dict["total_limit"], "1500")
        self.assertEqual(budget_dict["category_limits"]["Groceries"], "400")
        self.assertEqual(budget_dict["category_limits"]["Dining"], "200")
    
    def test_from_dict(self):
        """Test creating budget from dictionary."""
        start_date = datetime(2025, 5, 1)
        end_date = datetime(2025, 5, 31)
        
        budget_dict = {
            "name": "May 2025",
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "category_limits": {
                "Groceries": "400",
                "Dining": "200"
            },
            "budget_id": 1,
            "total_limit": "1500"
        }
        
        budget = Budget.from_dict(budget_dict)
        
        self.assertEqual(budget.name, "May 2025")
        self.assertEqual(budget.start_date, start_date)
        self.assertEqual(budget.end_date, end_date)
        self.assertEqual(budget.budget_id, 1)
        self.assertEqual(budget.total_limit, Decimal('1500'))
        self.assertEqual(budget.category_limits["Groceries"], Decimal('400'))
        self.assertEqual(budget.category_limits["Dining"], Decimal('200'))


if __name__ == '__main__':
    unittest.main()