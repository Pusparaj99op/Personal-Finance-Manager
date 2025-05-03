"""
Import/export functionality for the finance tracker application.
"""
import csv
import json
import datetime
from decimal import Decimal
from pathlib import Path
from typing import List, Dict, Any, Union, Optional

from finance_tracker.models.transaction import Transaction
from finance_tracker.models.category import Category
from finance_tracker.models.budget import Budget


def export_transactions_to_csv(
    transactions: List[Transaction], 
    filepath: str
) -> bool:
    """
    Export transactions to a CSV file.
    
    Args:
        transactions: List of Transaction objects to export
        filepath: Path to the output CSV file
    
    Returns:
        True if successful, False otherwise
    """
    try:
        with open(filepath, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            
            # Write header row
            writer.writerow([
                'transaction_id', 
                'amount', 
                'category', 
                'description', 
                'date', 
                'type'
            ])
            
            # Write transaction data
            for tx in transactions:
                writer.writerow([
                    tx.transaction_id,
                    str(tx.amount),
                    tx.category,
                    tx.description,
                    tx.transaction_date.strftime('%Y-%m-%d'),
                    tx.transaction_type
                ])
                
        return True
    except Exception as e:
        print(f"Error exporting transactions to CSV: {e}")
        return False


def import_transactions_from_csv(filepath: str) -> List[Dict[str, Any]]:
    """
    Import transactions from a CSV file.
    
    Expected CSV format:
    transaction_id,amount,category,description,date,type
    
    Args:
        filepath: Path to the CSV file
    
    Returns:
        List of dictionaries with transaction data that can be used to create Transaction objects
    """
    transactions = []
    
    try:
        with open(filepath, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            
            # Skip header row
            next(reader, None)
            
            for row in reader:
                if len(row) >= 5:  # Ensure we have at least the required fields
                    # Extract fields
                    try:
                        transaction_id = int(row[0]) if row[0] and row[0].isdigit() else None
                        amount = Decimal(row[1]) if row[1] else Decimal('0')
                        category = row[2] if row[2] else 'Uncategorized'
                        description = row[3] if row[3] else ''
                        
                        # Parse date
                        date_str = row[4] if len(row) > 4 and row[4] else datetime.datetime.now().strftime('%Y-%m-%d')
                        try:
                            date = datetime.datetime.strptime(date_str, '%Y-%m-%d')
                        except ValueError:
                            date = datetime.datetime.now()
                            
                        # Get transaction type
                        tx_type = row[5].lower() if len(row) > 5 and row[5] else 'expense'
                        if tx_type not in ['expense', 'income']:
                            tx_type = 'expense'
                        
                        # Create transaction data dictionary
                        transaction = {
                            'amount': amount,
                            'category': category,
                            'description': description,
                            'transaction_date': date,
                            'transaction_type': tx_type
                        }
                        
                        if transaction_id is not None:
                            transaction['transaction_id'] = transaction_id
                            
                        transactions.append(transaction)
                    except (ValueError, IndexError) as e:
                        print(f"Error parsing row {row}: {e}")
                        continue
        
        return transactions
    except Exception as e:
        print(f"Error importing transactions from CSV: {e}")
        return []


def export_to_json(
    transactions: List[Transaction] = None,
    categories: List[Category] = None,
    budgets: List[Budget] = None,
    filepath: str = None
) -> bool:
    """
    Export data to a JSON file.
    
    Args:
        transactions: Optional list of Transaction objects
        categories: Optional list of Category objects
        budgets: Optional list of Budget objects
        filepath: Path to the output JSON file
    
    Returns:
        True if successful, False otherwise
    """
    if not any([transactions, categories, budgets]):
        print("No data provided for export")
        return False
    
    if not filepath:
        filepath = f"finance_export_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    data = {}
    
    # Add transactions if provided
    if transactions:
        data['transactions'] = [tx.to_dict() for tx in transactions]
    
    # Add categories if provided
    if categories:
        data['categories'] = [cat.to_dict() for cat in categories]
    
    # Add budgets if provided
    if budgets:
        data['budgets'] = [budget.to_dict() for budget in budgets]
    
    try:
        with open(filepath, 'w') as jsonfile:
            # Convert Decimal to string for JSON serialization
            json.dump(data, jsonfile, indent=2, default=str)
        return True
    except Exception as e:
        print(f"Error exporting data to JSON: {e}")
        return False


def import_from_json(filepath: str) -> Dict[str, List[Dict[str, Any]]]:
    """
    Import data from a JSON file.
    
    Args:
        filepath: Path to the JSON file
    
    Returns:
        Dictionary with keys 'transactions', 'categories', and 'budgets', 
        each containing a list of dictionaries with the corresponding data
    """
    result = {
        'transactions': [],
        'categories': [],
        'budgets': []
    }
    
    try:
        with open(filepath, 'r') as jsonfile:
            data = json.load(jsonfile)
        
        # Extract transactions
        if 'transactions' in data and isinstance(data['transactions'], list):
            result['transactions'] = data['transactions']
        
        # Extract categories
        if 'categories' in data and isinstance(data['categories'], list):
            result['categories'] = data['categories']
        
        # Extract budgets
        if 'budgets' in data and isinstance(data['budgets'], list):
            result['budgets'] = data['budgets']
        
        return result
    except Exception as e:
        print(f"Error importing data from JSON: {e}")
        return result


def export_to_excel(
    transactions: List[Transaction] = None,
    categories: List[Category] = None,
    budgets: List[Budget] = None,
    filepath: str = None
) -> bool:
    """
    Export data to an Excel file.
    
    Note: This function requires the openpyxl package to be installed.
    
    Args:
        transactions: Optional list of Transaction objects
        categories: Optional list of Category objects
        budgets: Optional list of Budget objects
        filepath: Path to the output Excel file
    
    Returns:
        True if successful, False otherwise
    """
    try:
        import pandas as pd
    except ImportError:
        print("Pandas is required for Excel export. Install it with: pip install pandas openpyxl")
        return False
    
    if not any([transactions, categories, budgets]):
        print("No data provided for export")
        return False
    
    if not filepath:
        filepath = f"finance_export_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    
    try:
        with pd.ExcelWriter(filepath) as writer:
            # Export transactions
            if transactions:
                tx_data = [tx.to_dict() for tx in transactions]
                tx_df = pd.DataFrame(tx_data)
                tx_df.to_excel(writer, sheet_name='Transactions', index=False)
            
            # Export categories
            if categories:
                cat_data = [cat.to_dict() for cat in categories]
                cat_df = pd.DataFrame(cat_data)
                cat_df.to_excel(writer, sheet_name='Categories', index=False)
            
            # Export budgets
            if budgets:
                budget_data = []
                budget_limits_data = []
                
                for budget in budgets:
                    # Basic budget data
                    budget_dict = budget.to_dict()
                    budget_dict.pop('category_limits')  # Handle separately
                    budget_data.append(budget_dict)
                    
                    # Budget category limits
                    budget_id = budget.budget_id
                    for category, limit in budget.category_limits.items():
                        budget_limits_data.append({
                            'budget_id': budget_id,
                            'category': category,
                            'limit': str(limit)
                        })
                
                # Create DataFrames and write to Excel
                budget_df = pd.DataFrame(budget_data)
                budget_df.to_excel(writer, sheet_name='Budgets', index=False)
                
                if budget_limits_data:
                    limits_df = pd.DataFrame(budget_limits_data)
                    limits_df.to_excel(writer, sheet_name='BudgetLimits', index=False)
        
        return True
    except Exception as e:
        print(f"Error exporting data to Excel: {e}")
        return False


def get_supported_formats() -> Dict[str, Dict[str, bool]]:
    """
    Get information about supported import/export formats.
    
    Returns:
        Dictionary with format information
    """
    formats = {
        'csv': {
            'export': True,
            'import': True,
            'description': 'Comma-Separated Values format, good for spreadsheets',
            'transactions': True,
            'categories': False,
            'budgets': False
        },
        'json': {
            'export': True,
            'import': True,
            'description': 'JavaScript Object Notation, preserves all data structures',
            'transactions': True,
            'categories': True,
            'budgets': True
        },
        'excel': {
            'export': True,
            'import': False,  # Not implemented yet
            'description': 'Microsoft Excel format, good for organization and sharing',
            'transactions': True,
            'categories': True,
            'budgets': True
        }
    }
    
    # Check if pandas and openpyxl are available for Excel support
    try:
        import pandas
        import openpyxl
    except ImportError:
        formats['excel']['export'] = False
        formats['excel']['description'] += ' (requires pandas and openpyxl packages)'
    
    return formats