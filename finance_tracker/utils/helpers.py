"""
Helper utilities for the finance tracker application.
"""
import os
import csv
import json
import datetime
from decimal import Decimal
from pathlib import Path
from typing import List, Dict, Any, Union, Optional

from finance_tracker.models.transaction import Transaction


def format_currency(amount: Union[Decimal, float, int], currency_symbol: str = "$") -> str:
    """
    Format a monetary amount with the appropriate currency symbol.
    
    Args:
        amount: The monetary amount to format
        currency_symbol: The currency symbol to use
    
    Returns:
        Formatted currency string
    """
    if amount < 0:
        return f"-{currency_symbol}{abs(amount):.2f}"
    else:
        return f"{currency_symbol}{amount:.2f}"


def parse_date_string(date_string: str, formats: List[str] = None) -> Optional[datetime.datetime]:
    """
    Parse a date string into a datetime object, trying multiple formats.
    
    Args:
        date_string: The date string to parse
        formats: List of date formats to try (if None, uses defaults)
    
    Returns:
        datetime object if parsing succeeds, None otherwise
    """
    if formats is None:
        formats = [
            "%Y-%m-%d",       # 2023-04-15
            "%d/%m/%Y",       # 15/04/2023
            "%m/%d/%Y",       # 04/15/2023
            "%d-%m-%Y",       # 15-04-2023
            "%m-%d-%Y",       # 04-15-2023
            "%d.%m.%Y",       # 15.04.2023
            "%B %d, %Y",      # April 15, 2023
            "%d %B %Y",       # 15 April 2023
            "%Y%m%d"          # 20230415
        ]
    
    for date_format in formats:
        try:
            return datetime.datetime.strptime(date_string, date_format)
        except ValueError:
            continue
    
    return None


def get_month_start_end(year: int, month: int) -> tuple:
    """
    Get the start and end dates for a given month.
    
    Args:
        year: The year
        month: The month (1-12)
    
    Returns:
        Tuple of (start_date, end_date) as datetime objects
    """
    start_date = datetime.datetime(year, month, 1)
    
    # Get the last day of the month
    if month == 12:
        end_date = datetime.datetime(year + 1, 1, 1) - datetime.timedelta(days=1)
    else:
        end_date = datetime.datetime(year, month + 1, 1) - datetime.timedelta(days=1)
    
    # Set to end of day
    end_date = datetime.datetime.combine(
        end_date.date(), 
        datetime.time(23, 59, 59)
    )
    
    return start_date, end_date


def export_transactions_to_csv(
    transactions: List[Transaction], 
    filename: str
) -> bool:
    """
    Export a list of transactions to a CSV file.
    
    Args:
        transactions: List of Transaction objects
        filename: Path to the output CSV file
    
    Returns:
        True if successful, False otherwise
    """
    try:
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = [
                'transaction_id', 'date', 'amount', 'category', 
                'description', 'type'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for tx in transactions:
                writer.writerow({
                    'transaction_id': tx.transaction_id,
                    'date': tx.transaction_date.strftime('%Y-%m-%d'),
                    'amount': str(tx.amount),
                    'category': tx.category,
                    'description': tx.description,
                    'type': tx.transaction_type
                })
        
        return True
    except Exception as e:
        print(f"Error exporting transactions to CSV: {e}")
        return False


def import_transactions_from_csv(filename: str) -> List[Dict[str, Any]]:
    """
    Import transactions from a CSV file.
    
    Args:
        filename: Path to the CSV file
    
    Returns:
        List of dictionaries with transaction data
    """
    transactions = []
    
    try:
        with open(filename, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            
            for row in reader:
                # Convert date string to datetime
                date_str = row.get('date')
                if date_str:
                    date = parse_date_string(date_str)
                else:
                    date = datetime.datetime.now()
                
                # Create transaction dict
                transaction = {
                    'amount': row.get('amount'),
                    'category': row.get('category', 'Uncategorized'),
                    'description': row.get('description', ''),
                    'transaction_date': date.isoformat() if date else datetime.datetime.now().isoformat(),
                    'transaction_type': row.get('type', 'expense')
                }
                
                # Add transaction ID if present
                if 'transaction_id' in row and row['transaction_id']:
                    transaction['transaction_id'] = int(row['transaction_id'])
                
                transactions.append(transaction)
        
        return transactions
    except Exception as e:
        print(f"Error importing transactions from CSV: {e}")
        return []


def backup_database(db_path: str, backup_dir: str = None) -> str:
    """
    Create a backup of the database file.
    
    Args:
        db_path: Path to the database file
        backup_dir: Directory to store backups (if None, uses same directory as db)
    
    Returns:
        Path to the backup file if successful, empty string otherwise
    """
    try:
        db_path = Path(db_path)
        
        # Default backup directory is same as database
        if backup_dir is None:
            backup_dir = db_path.parent
        else:
            backup_dir = Path(backup_dir)
            backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate backup filename with timestamp
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"{db_path.stem}_backup_{timestamp}{db_path.suffix}"
        backup_path = backup_dir / backup_filename
        
        # Copy database file to backup
        import shutil
        shutil.copy2(db_path, backup_path)
        
        return str(backup_path)
    except Exception as e:
        print(f"Error creating database backup: {e}")
        return ""


def calculate_date_range(period: str) -> tuple:
    """
    Calculate start and end dates for common time periods.
    
    Args:
        period: String specifying the period ('month', 'quarter', 'year', 'ytd', etc.)
    
    Returns:
        Tuple of (start_date, end_date) as datetime objects
    """
    today = datetime.datetime.now()
    end_date = today
    
    if period == 'month' or period == 'current_month':
        start_date = datetime.datetime(today.year, today.month, 1)
    
    elif period == 'previous_month':
        if today.month == 1:
            start_date = datetime.datetime(today.year - 1, 12, 1)
            end_date = datetime.datetime(today.year, 1, 1) - datetime.timedelta(days=1)
        else:
            start_date = datetime.datetime(today.year, today.month - 1, 1)
            end_date = datetime.datetime(today.year, today.month, 1) - datetime.timedelta(days=1)
    
    elif period == 'quarter' or period == 'current_quarter':
        current_quarter = (today.month - 1) // 3 + 1
        start_month = (current_quarter - 1) * 3 + 1
        start_date = datetime.datetime(today.year, start_month, 1)
    
    elif period == 'year' or period == 'current_year':
        start_date = datetime.datetime(today.year, 1, 1)
    
    elif period == 'previous_year':
        start_date = datetime.datetime(today.year - 1, 1, 1)
        end_date = datetime.datetime(today.year, 1, 1) - datetime.timedelta(days=1)
    
    elif period == 'ytd' or period == 'year_to_date':
        start_date = datetime.datetime(today.year, 1, 1)
    
    elif period == 'last_30_days':
        start_date = today - datetime.timedelta(days=30)
    
    elif period == 'last_90_days':
        start_date = today - datetime.timedelta(days=90)
    
    elif period == 'last_6_months':
        if today.month <= 6:
            start_month = 7 + today.month - 6
            start_date = datetime.datetime(today.year - 1, start_month, 1)
        else:
            start_date = datetime.datetime(today.year, today.month - 5, 1)
    
    elif period == 'last_12_months':
        if today.month == 12:
            start_date = datetime.datetime(today.year, 1, 1)
        else:
            start_date = datetime.datetime(today.year - 1, today.month + 1, 1)
    
    else:
        # Default to current month
        start_date = datetime.datetime(today.year, today.month, 1)
    
    return start_date, end_date


def generate_report_filename(report_type: str, period: str) -> str:
    """
    Generate a filename for a report based on type and period.
    
    Args:
        report_type: Type of report (e.g., 'spending', 'budget', 'trends')
        period: Time period of the report
    
    Returns:
        Filename for the report
    """
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{report_type}_{period}_{timestamp}.pdf"