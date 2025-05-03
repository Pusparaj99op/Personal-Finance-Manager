"""
Unit tests for the finance tracker analysis modules.
"""
import unittest
from decimal import Decimal
from datetime import datetime, timedelta

from finance_tracker.models.transaction import Transaction
from finance_tracker.analysis.trends import (
    analyze_spending_trends,
    identify_unusual_expenses,
    analyze_recurring_expenses
)
from finance_tracker.analysis.patterns import (
    identify_spending_cycles,
    identify_impulse_purchases,
    identify_category_drift
)


class TestTrends(unittest.TestCase):
    """Tests for the trends module."""
    
    def setUp(self):
        """Set up test data."""
        # Create sample transactions for the last 6 months
        self.transactions = []
        base_date = datetime.now().replace(day=1) - timedelta(days=180)
        
        # Add grocery transactions (recurring weekly)
        for i in range(26):  # ~26 weeks in 6 months
            self.transactions.append(
                Transaction(
                    amount=75.50,
                    category="Groceries",
                    description="Weekly grocery shopping",
                    transaction_date=base_date + timedelta(days=i*7),
                    transaction_type="expense",
                    transaction_id=i+1
                )
            )
        
        # Add dining out transactions (sporadic)
        dining_dates = [5, 17, 32, 45, 68, 92, 110, 145, 160]
        for i, days in enumerate(dining_dates):
            self.transactions.append(
                Transaction(
                    amount=45.25,
                    category="Dining",
                    description="Restaurant",
                    transaction_date=base_date + timedelta(days=days),
                    transaction_type="expense",
                    transaction_id=100+i
                )
            )
        
        # Add monthly rent payments
        for i in range(6):
            self.transactions.append(
                Transaction(
                    amount=1200,
                    category="Housing",
                    description="Monthly rent",
                    transaction_date=base_date + timedelta(days=i*30),
                    transaction_type="expense",
                    transaction_id=200+i
                )
            )
        
        # Add a couple of unusual expenses
        self.transactions.append(
            Transaction(
                amount=850,
                category="Electronics",
                description="New smartphone",
                transaction_date=base_date + timedelta(days=45),
                transaction_type="expense",
                transaction_id=300
            )
        )
        
        self.transactions.append(
            Transaction(
                amount=350,
                category="Clothing",
                description="Winter jacket",
                transaction_date=base_date + timedelta(days=120),
                transaction_type="expense",
                transaction_id=301
            )
        )
        
        # Add income transactions
        for i in range(6):
            self.transactions.append(
                Transaction(
                    amount=3500,
                    category="Salary",
                    description="Monthly salary",
                    transaction_date=base_date + timedelta(days=i*30 + 1),
                    transaction_type="income",
                    transaction_id=400+i
                )
            )
    
    def test_analyze_spending_trends(self):
        """Test analyze_spending_trends function."""
        trends = analyze_spending_trends(self.transactions)
        
        # Check that we have valid output
        self.assertIn('total_spending', trends)
        self.assertIn('avg_monthly_spending', trends)
        self.assertIn('spending_trend', trends)
        self.assertIn('top_categories', trends)
        
        # Check that total spending is calculated correctly
        expected_total = sum(
            tx.amount for tx in self.transactions 
            if tx.transaction_type == 'expense'
        )
        self.assertEqual(trends['total_spending'], expected_total)
        
        # Check that top categories are present
        self.assertTrue(any(cat == 'Housing' for cat, _ in trends['top_categories']))
        self.assertTrue(any(cat == 'Groceries' for cat, _ in trends['top_categories']))
    
    def test_identify_unusual_expenses(self):
        """Test identify_unusual_expenses function."""
        unusual = identify_unusual_expenses(self.transactions)
        
        # Check that we found the unusual expenses
        self.assertTrue(any(tx.description == 'New smartphone' for tx in unusual))
        self.assertTrue(any(tx.category == 'Electronics' for tx in unusual))
    
    def test_analyze_recurring_expenses(self):
        """Test analyze_recurring_expenses function."""
        recurring = analyze_recurring_expenses(self.transactions)
        
        # Check that we have the expected structure
        self.assertIn('monthly', recurring)
        self.assertIn('weekly', recurring)
        
        # Check that we found the recurring expenses
        self.assertTrue(any(
            rec['description'] == 'Monthly rent' 
            for rec in recurring['monthly']
        ))
        self.assertTrue(any(
            rec['description'] == 'Weekly grocery shopping' 
            for rec in recurring['weekly']
        ))


class TestPatterns(unittest.TestCase):
    """Tests for the patterns module."""
    
    def setUp(self):
        """Set up test data."""
        # Create sample transactions for the last 3 months
        self.transactions = []
        base_date = datetime.now().replace(day=1) - timedelta(days=90)
        
        # Add weekly gym membership
        for i in range(13):  # ~13 weeks in 3 months
            self.transactions.append(
                Transaction(
                    amount=15.00,
                    category="Fitness",
                    description="Gym membership",
                    transaction_date=base_date + timedelta(days=i*7),
                    transaction_type="expense",
                    transaction_id=i+1
                )
            )
        
        # Add monthly subscriptions
        subscription_desc = [
            "Netflix subscription", 
            "Spotify subscription", 
            "Cloud storage"
        ]
        subscription_amounts = [13.99, 9.99, 5.99]
        
        for i in range(3):  # 3 months
            for j, desc in enumerate(subscription_desc):
                self.transactions.append(
                    Transaction(
                        amount=subscription_amounts[j],
                        category="Subscriptions",
                        description=desc,
                        transaction_date=base_date + timedelta(days=i*30 + j),
                        transaction_type="expense",
                        transaction_id=100 + i*10 + j
                    )
                )
        
        # Add some regular grocery trips
        grocery_days = [3, 10, 17, 24, 31, 38, 45, 52, 59, 66, 73, 80, 87]
        grocery_amounts = [65.50, 72.30, 68.99, 70.25, 85.75, 62.10, 75.50,
                           69.99, 77.25, 64.50, 72.80, 68.50, 71.20]
        
        for i, day in enumerate(grocery_days):
            self.transactions.append(
                Transaction(
                    amount=grocery_amounts[i],
                    category="Groceries",
                    description="Weekly groceries",
                    transaction_date=base_date + timedelta(days=day),
                    transaction_type="expense",
                    transaction_id=200 + i
                )
            )
        
        # Add some impulse purchases
        self.transactions.append(
            Transaction(
                amount=199.99,
                category="Electronics",
                description="Wireless headphones",
                transaction_date=base_date + timedelta(days=22),
                transaction_type="expense",
                transaction_id=300
            )
        )
        
        self.transactions.append(
            Transaction(
                amount=149.50,
                category="Clothing",
                description="Designer shoes",
                transaction_date=base_date + timedelta(days=55),
                transaction_type="expense",
                transaction_id=301
            )
        )
        
        # Add regular small electronics purchases for comparison
        for i, day in enumerate([15, 45, 75]):
            self.transactions.append(
                Transaction(
                    amount=25.99,
                    category="Electronics",
                    description="Accessories",
                    transaction_date=base_date + timedelta(days=day),
                    transaction_type="expense",
                    transaction_id=400 + i
                )
            )
    
    def test_identify_spending_cycles(self):
        """Test identify_spending_cycles function."""
        cycles = identify_spending_cycles(self.transactions)
        
        # Check that we have the expected categories
        self.assertIn('weekly', cycles)
        self.assertIn('monthly', cycles)
        
        # Check that we found the recurring cycles
        weekly_desc = [cycle['description'] for cycle in cycles['weekly']]
        monthly_desc = [cycle['description'] for cycle in cycles['monthly']]
        
        self.assertIn('Gym membership', weekly_desc)
        self.assertIn('Weekly groceries', weekly_desc)
        
        for sub in ['Netflix subscription', 'Spotify subscription', 'Cloud storage']:
            self.assertIn(sub, monthly_desc)
    
    def test_identify_impulse_purchases(self):
        """Test identify_impulse_purchases function."""
        impulses = identify_impulse_purchases(self.transactions)
        
        # Check that we found the impulse purchases
        impulse_desc = [imp['description'] for imp in impulses]
        
        self.assertIn('Wireless headphones', impulse_desc)
        self.assertIn('Designer shoes', impulse_desc)
    
    def test_identify_category_drift(self):
        """Test identify_category_drift function with minimal test data."""
        # Create test transactions specifically for category drift
        # We need two distinct time periods with different spending patterns
        
        base_date = datetime.now() - timedelta(days=60)
        
        period1_txs = []
        period2_txs = []
        
        # Period 1: Higher grocery spending, lower dining
        for i in range(5):
            period1_txs.append(
                Transaction(
                    amount=80.00,
                    category="Groceries",
                    description="Grocery shopping",
                    transaction_date=base_date + timedelta(days=i*5),
                    transaction_type="expense",
                    transaction_id=500 + i
                )
            )
            
            period1_txs.append(
                Transaction(
                    amount=20.00,
                    category="Dining",
                    description="Restaurant",
                    transaction_date=base_date + timedelta(days=i*6),
                    transaction_type="expense",
                    transaction_id=510 + i
                )
            )
        
        # Period 2: Lower grocery spending, higher dining
        for i in range(5):
            period2_txs.append(
                Transaction(
                    amount=50.00,
                    category="Groceries",
                    description="Grocery shopping",
                    transaction_date=base_date + timedelta(days=30 + i*5),
                    transaction_type="expense",
                    transaction_id=600 + i
                )
            )
            
            period2_txs.append(
                Transaction(
                    amount=60.00,
                    category="Dining",
                    description="Restaurant",
                    transaction_date=base_date + timedelta(days=30 + i*6),
                    transaction_type="expense",
                    transaction_id=610 + i
                )
            )
        
        all_txs = period1_txs + period2_txs
        
        # Call the function with a smaller window size for our test data
        drift = identify_category_drift(all_txs, window_size=15, threshold_percent=20)
        
        # Check that we detected the category drifts
        drift_categories = [item['category'] for item in drift]
        
        self.assertIn('Groceries', drift_categories)
        self.assertIn('Dining', drift_categories)
        
        # Verify that Groceries is decreasing
        groceries_drift = next(item for item in drift if item['category'] == 'Groceries')
        self.assertEqual(groceries_drift['trend'], 'decreasing')
        
        # Verify that Dining is increasing
        dining_drift = next(item for item in drift if item['category'] == 'Dining')
        self.assertEqual(dining_drift['trend'], 'increasing')


if __name__ == '__main__':
    unittest.main()