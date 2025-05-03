"""
Database storage implementation for the finance tracker application.
"""
import os
import sqlite3
from datetime import datetime
from decimal import Decimal
from typing import List, Optional, Dict, Any, Union, Tuple

from finance_tracker.models.transaction import Transaction
from finance_tracker.models.category import Category, create_default_categories
from finance_tracker.models.budget import Budget


class DatabaseStorage:
    """
    SQLite database storage for the finance tracker application.
    """
    def __init__(self, db_path: str = 'finance_tracker.db'):
        """
        Initialize the database storage.
        
        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = db_path
        self._create_tables_if_not_exist()
        self._initialize_categories_if_empty()
    
    def _get_connection(self) -> sqlite3.Connection:
        """
        Get a database connection.
        
        Returns:
            A sqlite3 Connection object
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Makes rows accessible by column name
        return conn
    
    def _create_tables_if_not_exist(self) -> None:
        """Create database tables if they don't exist."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Categories table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            category_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category_type TEXT NOT NULL,
            parent_category TEXT,
            budget_limit REAL
        )
        ''')
        
        # Transactions table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT NOT NULL,
            transaction_date TEXT NOT NULL,
            transaction_type TEXT NOT NULL
        )
        ''')
        
        # Budgets table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS budgets (
            budget_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            total_limit TEXT
        )
        ''')
        
        # Budget category limits table (many-to-many relationship)
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS budget_category_limits (
            budget_id INTEGER,
            category TEXT NOT NULL,
            amount TEXT NOT NULL,
            FOREIGN KEY (budget_id) REFERENCES budgets(budget_id),
            PRIMARY KEY (budget_id, category)
        )
        ''')
        
        conn.commit()
        conn.close()
    
    def _initialize_categories_if_empty(self) -> None:
        """Initialize with default categories if the categories table is empty."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Check if categories table is empty
        cursor.execute("SELECT COUNT(*) FROM categories")
        count = cursor.fetchone()[0]
        
        if count == 0:
            # Add default categories
            default_categories = create_default_categories()
            for category in default_categories:
                cursor.execute(
                    """
                    INSERT INTO categories (name, category_type, parent_category, budget_limit)
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        category.name,
                        category.category_type,
                        category.parent_category,
                        category.budget_limit
                    )
                )
            
            conn.commit()
        
        conn.close()
    
    # Transaction operations
    
    def add_transaction(self, transaction: Transaction) -> int:
        """
        Add a new transaction to the database.
        
        Args:
            transaction: The Transaction object to add
        
        Returns:
            The ID of the newly added transaction
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """
            INSERT INTO transactions (amount, category, description, transaction_date, transaction_type)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                str(transaction.amount),
                transaction.category,
                transaction.description,
                transaction.transaction_date.isoformat(),
                transaction.transaction_type
            )
        )
        
        transaction_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return transaction_id
    
    def get_transaction(self, transaction_id: int) -> Optional[Transaction]:
        """
        Get a transaction by ID.
        
        Args:
            transaction_id: The ID of the transaction to get
        
        Returns:
            The Transaction object if found, None otherwise
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM transactions WHERE transaction_id = ?", (transaction_id,))
        row = cursor.fetchone()
        
        conn.close()
        
        if row:
            # Convert row to dictionary
            data = dict(row)
            data["transaction_date"] = data["transaction_date"]
            data["amount"] = data["amount"]
            data["transaction_id"] = transaction_id
            return Transaction.from_dict(data)
        
        return None
    
    def update_transaction(self, transaction: Transaction) -> bool:
        """
        Update an existing transaction.
        
        Args:
            transaction: The Transaction object with updated data
        
        Returns:
            True if successful, False otherwise
        """
        if transaction.transaction_id is None:
            return False
        
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """
            UPDATE transactions
            SET amount = ?, category = ?, description = ?, transaction_date = ?, transaction_type = ?
            WHERE transaction_id = ?
            """,
            (
                str(transaction.amount),
                transaction.category,
                transaction.description,
                transaction.transaction_date.isoformat(),
                transaction.transaction_type,
                transaction.transaction_id
            )
        )
        
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        
        return success
    
    def delete_transaction(self, transaction_id: int) -> bool:
        """
        Delete a transaction by ID.
        
        Args:
            transaction_id: The ID of the transaction to delete
        
        Returns:
            True if successful, False otherwise
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM transactions WHERE transaction_id = ?", (transaction_id,))
        
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        
        return success
    
    def get_all_transactions(
        self,
        start_date: Optional[Union[datetime, str]] = None,
        end_date: Optional[Union[datetime, str]] = None,
        category: Optional[str] = None,
        transaction_type: Optional[str] = None
    ) -> List[Transaction]:
        """
        Get all transactions with optional filtering.
        
        Args:
            start_date: Optional start date for filtering (can be datetime or string)
            end_date: Optional end date for filtering (can be datetime or string)
            category: Optional category for filtering
            transaction_type: Optional transaction type for filtering
        
        Returns:
            List of Transaction objects matching the criteria
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Build the query based on provided filters
        query = "SELECT * FROM transactions"
        params = []
        
        # Add filters
        filters = []
        if start_date:
            filters.append("transaction_date >= ?")
            # Convert to string if it's a datetime object
            if isinstance(start_date, datetime):
                params.append(start_date.isoformat())
            else:
                params.append(start_date)
        
        if end_date:
            filters.append("transaction_date <= ?")
            # Convert to string if it's a datetime object
            if isinstance(end_date, datetime):
                params.append(end_date.isoformat())
            else:
                params.append(end_date)
        
        if category:
            filters.append("category = ?")
            params.append(category)
        
        if transaction_type:
            filters.append("transaction_type = ?")
            params.append(transaction_type)
        
        if filters:
            query += " WHERE " + " AND ".join(filters)
        
        # Add order by date (newest first)
        query += " ORDER BY transaction_date DESC"
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        conn.close()
        
        # Convert rows to Transaction objects
        transactions = []
        for row in rows:
            data = dict(row)
            data["transaction_id"] = row["transaction_id"]
            transactions.append(Transaction.from_dict(data))
        
        return transactions
    
    # Category operations
    
    def add_category(self, category: Category) -> int:
        """
        Add a new category to the database.
        
        Args:
            category: The Category object to add
        
        Returns:
            The ID of the newly added category
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """
            INSERT INTO categories (name, category_type, parent_category, budget_limit)
            VALUES (?, ?, ?, ?)
            """,
            (
                category.name,
                category.category_type,
                category.parent_category,
                category.budget_limit
            )
        )
        
        category_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return category_id
    
    def get_category(self, category_id: int) -> Optional[Category]:
        """
        Get a category by ID.
        
        Args:
            category_id: The ID of the category to retrieve
            
        Returns:
            Category object if found, None otherwise
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM categories WHERE category_id = ?", (category_id,))
        row = cursor.fetchone()
        
        conn.close()
        
        if not row:
            return None
            
        data = dict(row)
        data["category_id"] = row["category_id"]
        return Category.from_dict(data)
    
    def update_category(self, category: Category) -> bool:
        """
        Update an existing category.
        
        Args:
            category: The Category object with updated data
            
        Returns:
            True if successful, False otherwise
        """
        if category.category_id is None:
            return False
            
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """
            UPDATE categories
            SET name = ?, category_type = ?, parent_category = ?, budget_limit = ?
            WHERE category_id = ?
            """,
            (
                category.name,
                category.category_type,
                category.parent_category,
                category.budget_limit,
                category.category_id
            )
        )
        
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        
        return success
        
    def delete_category(self, category_id: int) -> bool:
        """
        Delete a category by ID and move associated transactions to 'Uncategorized'.
        
        Args:
            category_id: The ID of the category to delete
            
        Returns:
            True if successful, False otherwise
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # First, get the category name to update associated transactions
        cursor.execute("SELECT name FROM categories WHERE category_id = ?", (category_id,))
        row = cursor.fetchone()
        
        if not row:
            conn.close()
            return False
            
        category_name = row["name"]
        
        # Update transactions to use 'Uncategorized' category
        cursor.execute(
            "UPDATE transactions SET category = 'Uncategorized' WHERE category = ?", 
            (category_name,)
        )
        
        # Delete the category
        cursor.execute("DELETE FROM categories WHERE category_id = ?", (category_id,))
        
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        
        return success
    
    def get_all_categories(self, category_type: Optional[str] = None) -> List[Category]:
        """
        Get all categories with optional filtering by type.
        
        Args:
            category_type: Optional category type for filtering
        
        Returns:
            List of Category objects matching the criteria
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        query = "SELECT * FROM categories"
        params = []
        
        if category_type:
            query += " WHERE category_type = ?"
            params.append(category_type)
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        conn.close()
        
        # Convert rows to Category objects
        categories = []
        for row in rows:
            data = dict(row)
            data["category_id"] = row["category_id"]
            categories.append(Category.from_dict(data))
        
        return categories
    
    # Budget operations
    
    def add_budget(self, budget: Budget) -> int:
        """
        Add a new budget to the database.
        
        Args:
            budget: The Budget object to add
        
        Returns:
            The ID of the newly added budget
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Insert budget
        cursor.execute(
            """
            INSERT INTO budgets (name, start_date, end_date, total_limit)
            VALUES (?, ?, ?, ?)
            """,
            (
                budget.name,
                budget.start_date.isoformat(),
                budget.end_date.isoformat(),
                str(budget.total_limit) if budget.total_limit else None
            )
        )
        
        budget_id = cursor.lastrowid
        
        # Insert budget category limits
        for category, amount in budget.category_limits.items():
            cursor.execute(
                """
                INSERT INTO budget_category_limits (budget_id, category, amount)
                VALUES (?, ?, ?)
                """,
                (budget_id, category, str(amount))
            )
        
        conn.commit()
        conn.close()
        
        return budget_id
    
    def get_budget(self, budget_id: int) -> Optional[Budget]:
        """
        Get a budget by ID.
        
        Args:
            budget_id: The ID of the budget to get
        
        Returns:
            The Budget object if found, None otherwise
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Get budget data
        cursor.execute("SELECT * FROM budgets WHERE budget_id = ?", (budget_id,))
        budget_row = cursor.fetchone()
        
        if not budget_row:
            conn.close()
            return None
        
        # Get budget category limits
        cursor.execute(
            "SELECT category, amount FROM budget_category_limits WHERE budget_id = ?",
            (budget_id,)
        )
        limit_rows = cursor.fetchall()
        
        conn.close()
        
        # Build category limits dictionary
        category_limits = {row["category"]: Decimal(row["amount"]) for row in limit_rows}
        
        # Create Budget object
        budget_data = dict(budget_row)
        budget = Budget(
            name=budget_data["name"],
            start_date=datetime.fromisoformat(budget_data["start_date"]),
            end_date=datetime.fromisoformat(budget_data["end_date"]),
            category_limits=category_limits,
            budget_id=budget_id,
            total_limit=Decimal(budget_data["total_limit"]) if budget_data.get("total_limit") else None
        )
        
        return budget
    
    def get_active_budget(self) -> Optional[Budget]:
        """
        Get the currently active budget.
        
        Returns:
            The active Budget object if found, None otherwise
        """
        now = datetime.now().isoformat()
        
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Get budget that includes current date
        cursor.execute(
            """
            SELECT * FROM budgets
            WHERE start_date <= ? AND end_date >= ?
            ORDER BY start_date DESC LIMIT 1
            """,
            (now, now)
        )
        budget_row = cursor.fetchone()
        
        if not budget_row:
            conn.close()
            return None
        
        budget_id = budget_row["budget_id"]
        
        # Get budget category limits
        cursor.execute(
            "SELECT category, amount FROM budget_category_limits WHERE budget_id = ?",
            (budget_id,)
        )
        limit_rows = cursor.fetchall()
        
        conn.close()
        
        # Build category limits dictionary
        category_limits = {row["category"]: Decimal(row["amount"]) for row in limit_rows}
        
        # Create Budget object
        budget_data = dict(budget_row)
        budget = Budget(
            name=budget_data["name"],
            start_date=datetime.fromisoformat(budget_data["start_date"]),
            end_date=datetime.fromisoformat(budget_data["end_date"]),
            category_limits=category_limits,
            budget_id=budget_id,
            total_limit=Decimal(budget_data["total_limit"]) if budget_data.get("total_limit") else None
        )
        
        return budget
    
    # Summary and analysis methods
    
    def get_category_spending_summary(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict[str, Decimal]:
        """
        Get summary of spending by category.
        
        Args:
            start_date: Optional start date for filtering
            end_date: Optional end date for filtering
        
        Returns:
            Dictionary mapping category names to total spent amounts
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Build the query based on provided filters
        query = """
            SELECT category, SUM(CAST(amount AS REAL)) as total
            FROM transactions
            WHERE transaction_type = 'expense'
        """
        params = []
        
        # Add date filters if provided
        if start_date:
            query += " AND transaction_date >= ?"
            params.append(start_date.isoformat())
        
        if end_date:
            query += " AND transaction_date <= ?"
            params.append(end_date.isoformat())
        
        # Group by category
        query += " GROUP BY category"
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        conn.close()
        
        # Convert to dictionary
        summary = {row["category"]: Decimal(str(row["total"])) for row in rows}
        
        return summary
    
    def get_monthly_spending(self, months: int = 12) -> Dict[str, Decimal]:
        """
        Get total spending by month for the last N months.
        
        Args:
            months: Number of months to include
        
        Returns:
            Dictionary mapping month strings (YYYY-MM) to total spent amounts
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # SQLite date functions to extract year and month
        query = """
            SELECT 
                strftime('%Y-%m', transaction_date) as month,
                SUM(CAST(amount AS REAL)) as total
            FROM transactions
            WHERE transaction_type = 'expense'
            GROUP BY month
            ORDER BY month DESC
            LIMIT ?
        """
        
        cursor.execute(query, (months,))
        rows = cursor.fetchall()
        
        conn.close()
        
        # Convert to dictionary
        monthly_spending = {row["month"]: Decimal(str(row["total"])) for row in rows}
        
        return monthly_spending
    
    def get_income_vs_expenses(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict[str, Decimal]:
        """
        Get total income and expenses for a period.
        
        Args:
            start_date: Optional start date for filtering
            end_date: Optional end date for filtering
        
        Returns:
            Dictionary with 'income', 'expenses', and 'balance' keys
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Build the query for both income and expenses
        query = """
            SELECT 
                transaction_type,
                SUM(CAST(amount AS REAL)) as total
            FROM transactions
        """
        params = []
        
        # Add date filters if provided
        filters = []
        if start_date:
            filters.append("transaction_date >= ?")
            params.append(start_date.isoformat())
        
        if end_date:
            filters.append("transaction_date <= ?")
            params.append(end_date.isoformat())
        
        if filters:
            query += " WHERE " + " AND ".join(filters)
        
        # Group by transaction type
        query += " GROUP BY transaction_type"
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        conn.close()
        
        # Initialize with zeros
        result = {"income": Decimal('0'), "expenses": Decimal('0')}
        
        # Populate from results
        for row in rows:
            if row["transaction_type"] == "income":
                result["income"] = Decimal(str(row["total"]))
            elif row["transaction_type"] == "expense":
                result["expenses"] = Decimal(str(row["total"]))
        
        # Calculate balance
        result["balance"] = result["income"] - result["expenses"]
        
        return result