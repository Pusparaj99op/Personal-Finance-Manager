"""
Trends analysis module for the finance tracker application.
"""
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple, Any, Union
from decimal import Decimal
import calendar
from collections import defaultdict

import pandas as pd
import numpy as np
from finance_tracker.models.transaction import Transaction


def analyze_spending_trends(
    transactions: List[Transaction],
    period_months: int = 6
) -> Dict[str, Any]:
    """
    Analyze spending trends over time.
    
    Args:
        transactions: List of Transaction objects
        period_months: Number of months to analyze
    
    Returns:
        Dictionary with trend analysis results
    """
    # Convert transactions to DataFrame for easier analysis
    df = transactions_to_dataframe(transactions)
    
    # Check if DataFrame is empty or missing required columns
    if df.empty or 'transaction_date' not in df.columns:
        return {
            "total_spending": Decimal('0'),
            "avg_monthly_spending": Decimal('0'),
            "top_categories": [],
            "month_over_month_change": Decimal('0'),
            "spending_trend": "neutral",
            "highest_spending_day": None,
            "highest_spending_month": None
        }
    
    # Check if transaction_type column exists, if not create it
    if 'transaction_type' not in df.columns:
        # Add the transaction_type column based on Transaction object attributes
        transaction_types = []
        for transaction in transactions:
            if hasattr(transaction, 'transaction_type'):
                transaction_types.append(transaction.transaction_type)
            else:
                transaction_types.append('expense')  # Default to expense
        
        # If DataFrame and transactions list have the same length, add the column
        if len(df) == len(transaction_types):
            df['transaction_type'] = transaction_types
        else:
            # If lengths don't match, add a default value
            df['transaction_type'] = 'expense'
    
    # Filter to only include expenses from the relevant period
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30 * period_months)
    
    expense_df = df[
        (df['transaction_type'] == 'expense') &
        (df['transaction_date'] >= start_date) &
        (df['transaction_date'] <= end_date)
    ]
    
    if expense_df.empty:
        return {
            "total_spending": Decimal('0'),
            "avg_monthly_spending": Decimal('0'),
            "top_categories": [],
            "month_over_month_change": Decimal('0'),
            "spending_trend": "neutral",
            "highest_spending_day": None,
            "highest_spending_month": None
        }
    
    # Calculate total spending
    total_spending = Decimal(str(expense_df['amount'].sum()))
    
    # Calculate average monthly spending
    months_in_data = min(period_months, 
                         (expense_df['transaction_date'].max() - 
                          expense_df['transaction_date'].min()).days / 30)
    months_in_data = max(1, months_in_data)  # Ensure we don't divide by zero
    avg_monthly_spending = total_spending / Decimal(str(months_in_data))
    
    # Find top spending categories
    top_categories = expense_df.groupby('category')['amount'].sum().sort_values(ascending=False)
    top_categories = [(cat, Decimal(str(amount))) for cat, amount in top_categories.items()]
    
    # Calculate month-over-month change
    expense_df['month'] = expense_df['transaction_date'].dt.strftime('%Y-%m')
    monthly_spending = expense_df.groupby('month')['amount'].sum()
    
    if len(monthly_spending) >= 2:
        current_month = monthly_spending.index[-1]
        previous_month = monthly_spending.index[-2]
        
        current_month_spending = monthly_spending[current_month]
        previous_month_spending = monthly_spending[previous_month]
        
        if previous_month_spending > 0:
            month_over_month_change = Decimal(str((current_month_spending - previous_month_spending) / 
                                           previous_month_spending * 100))
        else:
            month_over_month_change = Decimal('100')  # If there was no spending last month
    else:
        month_over_month_change = Decimal('0')
    
    # Determine spending trend
    if len(monthly_spending) >= 3:
        recent_months = monthly_spending.iloc[-3:].values
        if recent_months[2] > recent_months[1] > recent_months[0]:
            spending_trend = "increasing"
        elif recent_months[2] < recent_months[1] < recent_months[0]:
            spending_trend = "decreasing"
        else:
            spending_trend = "fluctuating"
    else:
        spending_trend = "neutral"
    
    # Find highest spending day of week
    expense_df['day_of_week'] = expense_df['transaction_date'].dt.day_name()
    day_spending = expense_df.groupby('day_of_week')['amount'].sum()
    if not day_spending.empty:
        highest_spending_day = day_spending.idxmax()
    else:
        highest_spending_day = None
    
    # Find highest spending month
    month_spending = expense_df.groupby(expense_df['transaction_date'].dt.month)['amount'].sum()
    if not month_spending.empty:
        highest_month_num = month_spending.idxmax()
        highest_spending_month = calendar.month_name[highest_month_num]
    else:
        highest_spending_month = None
    
    return {
        "total_spending": total_spending,
        "avg_monthly_spending": avg_monthly_spending,
        "top_categories": top_categories[:5],  # Top 5 categories
        "month_over_month_change": month_over_month_change,
        "spending_trend": spending_trend,
        "highest_spending_day": highest_spending_day,
        "highest_spending_month": highest_spending_month
    }


def identify_unusual_expenses(
    transactions: List[Transaction],
    threshold_multiplier: float = 2.0
) -> List[Transaction]:
    """
    Identify unusually high expenses compared to category averages.
    
    Args:
        transactions: List of Transaction objects
        threshold_multiplier: How many times above average to flag as unusual
    
    Returns:
        List of Transaction objects representing unusual expenses
    """
    # Convert transactions to DataFrame
    df = transactions_to_dataframe(transactions)
    
    # Check if DataFrame is empty or missing required columns
    if df.empty or 'transaction_date' not in df.columns or 'category' not in df.columns:
        return []
    
    # Check if transaction_type column exists, if not create it
    if 'transaction_type' not in df.columns:
        df['transaction_type'] = 'expense'  # Default all to expense
    
    # Filter to only include expenses
    expense_df = df[df['transaction_type'] == 'expense']
    
    if expense_df.empty:
        return []
    
    # Calculate average spending by category
    category_avg = expense_df.groupby('category')['amount'].mean()
    
    # Find transactions that exceed the threshold
    unusual_expenses = []
    
    for _, row in expense_df.iterrows():
        try:
            category = row['category']
            amount = row['amount']
            
            # If category only has one transaction, we can't determine if it's unusual
            if category in category_avg:
                avg_for_category = category_avg[category]
                
                # Check if significantly higher than average
                if amount > avg_for_category * threshold_multiplier:
                    # Find the original Transaction object
                    transaction_id = row.get('transaction_id')
                    if transaction_id is not None:
                        for transaction in transactions:
                            if hasattr(transaction, 'transaction_id') and transaction.transaction_id == transaction_id:
                                unusual_expenses.append(transaction)
                                break
        except (KeyError, TypeError, AttributeError):
            # Skip problematic rows
            continue
    
    return unusual_expenses


def analyze_recurring_expenses(
    transactions: List[Transaction],
    min_occurrences: int = 2
) -> Dict[str, List[Dict]]:
    """
    Identify recurring expenses by pattern matching.
    
    Args:
        transactions: List of Transaction objects
        min_occurrences: Minimum occurrences to consider a recurring expense
    
    Returns:
        Dictionary with lists of potential recurring expenses by frequency
    """
    # Convert transactions to DataFrame
    df = transactions_to_dataframe(transactions)
    
    # Check if DataFrame is empty or missing required columns
    if df.empty or 'transaction_date' not in df.columns:
        return {"monthly": [], "weekly": [], "other": []}
    
    # Check if transaction_type column exists, if not create it
    if 'transaction_type' not in df.columns:
        df['transaction_type'] = 'expense'  # Default all to expense
    
    # Filter to only include expenses
    expense_df = df[df['transaction_type'] == 'expense']
    
    if expense_df.empty:
        return {"monthly": [], "weekly": [], "other": []}
    
    # Sort by date
    expense_df = expense_df.sort_values('transaction_date')
    
    # Group potentially recurring expenses (similar description, amount, category)
    potential_recurring = defaultdict(list)
    
    for _, row in expense_df.iterrows():
        try:
            key = f"{row['description']}-{row['category']}"
            potential_recurring[key].append({
                "transaction_id": row.get('transaction_id'),
                "amount": row.get('amount', 0),
                "date": row.get('transaction_date', datetime.now()),
                "description": row.get('description', ''),
                "category": row.get('category', 'Uncategorized')
            })
        except (KeyError, TypeError, AttributeError):
            # Skip problematic rows
            continue
    
    # Filter out groups with too few occurrences
    recurring = {
        key: transactions 
        for key, transactions in potential_recurring.items() 
        if len(transactions) >= min_occurrences
    }
    
    # Classify by frequency
    result = {"monthly": [], "weekly": [], "other": []}
    
    for group_key, group_transactions in recurring.items():
        if len(group_transactions) < 2:
            continue
        
        try:    
            # Calculate average time between transactions
            dates = [t["date"] for t in group_transactions]
            deltas = [(dates[i] - dates[i-1]).days for i in range(1, len(dates))]
            if not deltas:
                continue
            
            avg_delta = sum(deltas) / len(deltas)
            
            # Calculate average amount safely
            amounts = [float(t.get("amount", 0)) for t in group_transactions]
            if not amounts:
                avg_amount = 0
            else:
                avg_amount = sum(amounts) / len(amounts)
            
            # Get a safe last date
            try:
                last_date = max(dates).strftime("%Y-%m-%d")
            except (ValueError, AttributeError):
                last_date = datetime.now().strftime("%Y-%m-%d")
            
            # Common attributes for all types
            base_record = {
                "description": group_transactions[0].get("description", ""),
                "category": group_transactions[0].get("category", "Uncategorized"),
                "avg_amount": avg_amount,
                "occurrences": len(group_transactions),
                "last_date": last_date
            }
            
            # Classify by average delta
            if 25 <= avg_delta <= 35:  # Monthly
                result["monthly"].append(base_record)
            elif 5 <= avg_delta <= 9:  # Weekly
                result["weekly"].append(base_record)
            else:  # Other periodic
                other_record = base_record.copy()
                other_record["avg_days_between"] = avg_delta
                result["other"].append(other_record)
                
        except (ValueError, TypeError, AttributeError, IndexError, ZeroDivisionError) as e:
            # Skip problematic transaction groups
            continue
    
    return result


def forecast_monthly_expenses(
    transactions: List[Transaction], 
    months_ahead: int = 3
) -> Dict[str, Decimal]:
    """
    Forecast monthly expenses based on historical data.
    
    Args:
        transactions: List of Transaction objects
        months_ahead: Number of months ahead to forecast
    
    Returns:
        Dictionary mapping future months to forecasted expense amounts
    """
    # Convert transactions to DataFrame
    df = transactions_to_dataframe(transactions)
    
    # Check if DataFrame is empty or missing required columns
    if df.empty or 'transaction_date' not in df.columns:
        return {}
    
    # Check if transaction_type column exists, if not create it
    if 'transaction_type' not in df.columns:
        df['transaction_type'] = 'expense'  # Default all to expense
    
    # Filter to only include expenses
    expense_df = df[df['transaction_type'] == 'expense']
    
    if expense_df.empty:
        return {}
    
    # Group by month and calculate total
    expense_df['month'] = expense_df['transaction_date'].dt.strftime('%Y-%m')
    monthly_totals = expense_df.groupby('month')['amount'].sum()
    
    if len(monthly_totals) < 2:
        # Not enough data for forecasting, use the average of available data
        avg_monthly = Decimal(str(monthly_totals.mean())) if not monthly_totals.empty else Decimal('0')
        forecast = {}
        current_date = datetime.now()
        
        for i in range(1, months_ahead + 1):
            future_date = current_date + timedelta(days=30 * i)
            future_month = future_date.strftime('%Y-%m')
            forecast[future_month] = avg_monthly
            
        return forecast
    
    # Use simple moving average for forecasting
    # For a more sophisticated approach, consider using pandas or statsmodels for time series forecasting
    recent_months = min(6, len(monthly_totals))  # Use up to 6 months of data
    recent_avg = Decimal(str(monthly_totals[-recent_months:].mean()))
    
    # Calculate month-over-month growth rate
    growth_rates = []
    for i in range(1, len(monthly_totals)):
        if monthly_totals.iloc[i-1] > 0:
            growth_rate = (monthly_totals.iloc[i] - monthly_totals.iloc[i-1]) / monthly_totals.iloc[i-1]
            growth_rates.append(growth_rate)
    
    # Use average growth rate if available, otherwise assume flat
    if growth_rates:
        avg_growth_rate = Decimal(str(sum(growth_rates) / len(growth_rates)))
    else:
        avg_growth_rate = Decimal('0')
    
    # Generate forecast
    forecast = {}
    current_amount = Decimal(str(monthly_totals.iloc[-1]))
    current_date = datetime.now()
    
    for i in range(1, months_ahead + 1):
        current_amount = current_amount * (1 + avg_growth_rate)
        future_date = current_date + timedelta(days=30 * i)
        future_month = future_date.strftime('%Y-%m')
        forecast[future_month] = current_amount
    
    return forecast


def transactions_to_dataframe(transactions: List[Transaction]) -> pd.DataFrame:
    """
    Convert a list of Transaction objects to a pandas DataFrame for analysis.
    
    Args:
        transactions: List of Transaction objects
    
    Returns:
        Pandas DataFrame with transaction data
    """
    # Handle empty transactions list
    if not transactions:
        # Return empty DataFrame with expected columns
        return pd.DataFrame(columns=[
            'transaction_id', 'amount', 'category', 'description',
            'transaction_date', 'transaction_type'
        ])
    
    data = []
    for transaction in transactions:
        # Handle potentially missing attributes safely
        try:
            row_data = {
                'transaction_id': getattr(transaction, 'transaction_id', None),
                'amount': float(getattr(transaction, 'amount', 0)),
                'category': getattr(transaction, 'category', 'Uncategorized'),
                'description': getattr(transaction, 'description', ''),
                'transaction_date': getattr(transaction, 'transaction_date', datetime.now()),
                'transaction_type': getattr(transaction, 'transaction_type', 'expense')
            }
            data.append(row_data)
        except (ValueError, TypeError, AttributeError) as e:
            # Skip transactions with invalid data
            continue
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Ensure transaction_date is datetime
    if not df.empty and 'transaction_date' in df.columns:
        df['transaction_date'] = pd.to_datetime(df['transaction_date'], errors='coerce')
        # Replace NaT values with current date
        df['transaction_date'].fillna(datetime.now(), inplace=True)
    
    return df


def calculate_category_allocations(
    transactions: List[Transaction],
    months: int = 6
) -> Dict[str, float]:
    """
    Calculate recommended budget allocations based on historical spending.
    
    Args:
        transactions: List of Transaction objects
        months: Number of months of history to consider
    
    Returns:
        Dictionary mapping categories to recommended budget percentages
    """
    # Convert transactions to DataFrame
    df = transactions_to_dataframe(transactions)
    
    # Check if DataFrame is empty or missing required columns
    if df.empty or 'transaction_date' not in df.columns:
        return {}
    
    # Check if transaction_type column exists, if not create it
    if 'transaction_type' not in df.columns:
        df['transaction_type'] = 'expense'  # Default all to expense
    
    # Filter to only include expenses from recent months
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30 * months)
    
    try:
        expense_df = df[
            (df['transaction_type'] == 'expense') &
            (df['transaction_date'] >= start_date) &
            (df['transaction_date'] <= end_date)
        ]
    except Exception:
        # If filtering fails, return empty result
        return {}
    
    if expense_df.empty:
        return {}
    
    # Calculate total spending
    total_spending = expense_df['amount'].sum()
    
    # Prevent division by zero
    if total_spending == 0:
        return {}
    
    # Calculate spending by category
    category_spending = expense_df.groupby('category')['amount'].sum()
    
    # Convert to percentages
    category_percentages = {
        category: round((amount / total_spending) * 100, 1)
        for category, amount in category_spending.items()
    }
    
    return category_percentages