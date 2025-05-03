"""
Pattern identification module for the finance tracker application.

This module provides advanced analysis to identify patterns in spending behavior,
including cyclical spending, impulse purchases, and early warning signals.
"""
import calendar
import datetime
from decimal import Decimal
from typing import List, Dict, Any, Optional, Tuple, Union
from collections import defaultdict

import numpy as np
import pandas as pd
from finance_tracker.models.transaction import Transaction


def identify_spending_cycles(
    transactions: List[Transaction],
    min_periods: int = 3,
    max_variance_days: int = 3
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Identify recurring spending cycles by analyzing transaction patterns.
    
    Args:
        transactions: List of Transaction objects
        min_periods: Minimum number of occurrences to consider as a cycle
        max_variance_days: Maximum allowed variance in days between occurrences
    
    Returns:
        Dictionary mapping cycle types to lists of potential cycles
    """
    # Convert transactions to DataFrame for easier analysis
    df = _transactions_to_dataframe(transactions)
    
    # Filter to only include expenses
    expense_df = df[df['transaction_type'] == 'expense'].copy()
    
    if expense_df.empty:
        return {"weekly": [], "monthly": [], "quarterly": [], "other": []}
    
    # Sort by date
    expense_df.sort_values('transaction_date', inplace=True)
    
    # Group by description and category to find potential recurring transactions
    grouped = expense_df.groupby(['description', 'category'])
    
    cycles = {
        "weekly": [],
        "monthly": [], 
        "quarterly": [],
        "other": []
    }
    
    for (desc, cat), group in grouped:
        # Need at least min_periods occurrences
        if len(group) < min_periods:
            continue
        
        # Calculate days between consecutive transactions
        group = group.sort_values('transaction_date')
        dates = group['transaction_date'].tolist()
        
        # Calculate intervals between transactions in days
        intervals = [(dates[i] - dates[i-1]).days for i in range(1, len(dates))]
        
        # Skip if no intervals (only one transaction)
        if not intervals:
            continue
            
        # Calculate average interval and its variance
        avg_interval = sum(intervals) / len(intervals)
        variance = sum((interval - avg_interval) ** 2 for interval in intervals) / len(intervals)
        std_dev = variance ** 0.5
        
        # Skip if variance is too high
        if std_dev > max_variance_days:
            continue
        
        # Determine cycle type based on average interval
        cycle_type = "other"
        if 5 <= avg_interval <= 9:  # Weekly (with some flexibility)
            cycle_type = "weekly"
        elif 25 <= avg_interval <= 35:  # Monthly
            cycle_type = "monthly"
        elif 85 <= avg_interval <= 95:  # Quarterly
            cycle_type = "quarterly"
        
        # Add to appropriate cycle category
        cycles[cycle_type].append({
            "description": desc,
            "category": cat,
            "avg_amount": float(group['amount'].mean()),
            "avg_interval_days": avg_interval,
            "occurrences": len(group),
            "last_date": dates[-1].strftime("%Y-%m-%d"),
            "next_expected": (dates[-1] + datetime.timedelta(days=round(avg_interval))).strftime("%Y-%m-%d"),
            "std_dev_days": std_dev,
            "confidenceScore": _calculate_confidence_score(len(group), std_dev, max_variance_days)
        })
    
    # Sort each category by confidence score
    for cycle_type in cycles:
        cycles[cycle_type] = sorted(cycles[cycle_type], key=lambda x: x["confidenceScore"], reverse=True)
    
    return cycles


def identify_impulse_purchases(
    transactions: List[Transaction],
    threshold_multiplier: float = 1.75,
    min_amount: float = 0.0
) -> List[Dict[str, Any]]:
    """
    Identify potential impulse purchases based on spending patterns.
    
    Args:
        transactions: List of Transaction objects
        threshold_multiplier: Multiplier above average category spending to flag
        min_amount: Minimum amount to consider (to avoid flagging small purchases)
    
    Returns:
        List of dictionaries describing potential impulse purchases
    """
    # Convert transactions to DataFrame for easier analysis
    df = _transactions_to_dataframe(transactions)
    
    # Filter to only include expenses above minimum amount
    expense_df = df[(df['transaction_type'] == 'expense') & (df['amount'] >= min_amount)]
    
    if expense_df.empty:
        return []
    
    # Calculate average spending by category
    category_avg = expense_df.groupby('category')['amount'].mean()
    
    # Calculate standard deviation by category
    category_std = expense_df.groupby('category')['amount'].std().fillna(0)
    
    # Identify outliers
    impulse_purchases = []
    
    for idx, row in expense_df.iterrows():
        category = row['category']
        amount = row['amount']
        
        # Skip if we don't have enough data for this category
        if category not in category_avg or category_avg[category] == 0:
            continue
        
        # Calculate z-score if we have standard deviation
        if category in category_std and category_std[category] > 0:
            z_score = (amount - category_avg[category]) / category_std[category]
        else:
            z_score = 0
            
        # Check if significantly higher than average
        ratio = amount / category_avg[category]
        
        if ratio >= threshold_multiplier:
            # Find original transaction
            transaction = next(
                (t for t in transactions if t.transaction_id == row['transaction_id']),
                None
            )
            
            if transaction:
                impulse_purchases.append({
                    "transaction_id": transaction.transaction_id,
                    "description": transaction.description,
                    "category": transaction.category,
                    "amount": float(transaction.amount),
                    "date": transaction.transaction_date.strftime("%Y-%m-%d"),
                    "category_avg": float(category_avg[category]),
                    "ratio_to_avg": ratio,
                    "z_score": z_score,
                    "confidence": _calculate_impulse_confidence(ratio, z_score)
                })
    
    # Sort by confidence
    return sorted(impulse_purchases, key=lambda x: x["confidence"], reverse=True)


def identify_category_drift(
    transactions: List[Transaction],
    window_size: int = 30,
    threshold_percent: float = 30.0
) -> List[Dict[str, Any]]:
    """
    Identify categories with significant spending changes over time.
    
    Args:
        transactions: List of Transaction objects
        window_size: Size of comparison window in days
        threshold_percent: Minimum percent change to flag
        
    Returns:
        List of dictionaries describing category spending changes
    """
    # Convert transactions to DataFrame
    df = _transactions_to_dataframe(transactions)
    
    # Filter to only include expenses
    expense_df = df[df['transaction_type'] == 'expense']
    
    if len(expense_df) < 10:  # Need at least some data for meaningful comparison
        return []
    
    # Get date range
    earliest_date = expense_df['transaction_date'].min()
    latest_date = expense_df['transaction_date'].max()
    
    # Need at least 2*window_size days of data
    if (latest_date - earliest_date).days < 2 * window_size:
        return []
    
    # Define time periods for comparison
    period1_end = latest_date - datetime.timedelta(days=window_size)
    period1_start = period1_end - datetime.timedelta(days=window_size)
    
    period2_start = latest_date - datetime.timedelta(days=window_size)
    period2_end = latest_date
    
    # Filter data for each period
    period1_df = expense_df[
        (expense_df['transaction_date'] >= period1_start) & 
        (expense_df['transaction_date'] <= period1_end)
    ]
    
    period2_df = expense_df[
        (expense_df['transaction_date'] >= period2_start) & 
        (expense_df['transaction_date'] <= period2_end)
    ]
    
    # Calculate total spending by category for each period
    period1_spending = period1_df.groupby('category')['amount'].sum()
    period2_spending = period2_df.groupby('category')['amount'].sum()
    
    # Combine and calculate changes
    category_changes = []
    
    # Create a set of all categories across both periods
    all_categories = set(period1_spending.index) | set(period2_spending.index)
    
    for category in all_categories:
        p1_spent = float(period1_spending.get(category, 0))
        p2_spent = float(period2_spending.get(category, 0))
        
        # Skip categories with no spending in either period
        if p1_spent == 0 and p2_spent == 0:
            continue
            
        # Calculate percent change
        if p1_spent == 0:
            percent_change = 100  # New category
        else:
            percent_change = ((p2_spent - p1_spent) / p1_spent) * 100
        
        # Only include significant changes
        if abs(percent_change) >= threshold_percent:
            category_changes.append({
                "category": category,
                "previous_spending": p1_spent,
                "current_spending": p2_spent,
                "absolute_change": p2_spent - p1_spent,
                "percent_change": percent_change,
                "period1": f"{period1_start.strftime('%Y-%m-%d')} to {period1_end.strftime('%Y-%m-%d')}",
                "period2": f"{period2_start.strftime('%Y-%m-%d')} to {period2_end.strftime('%Y-%m-%d')}",
                "trend": "increasing" if percent_change > 0 else "decreasing"
            })
    
    # Sort by absolute percent change
    return sorted(category_changes, key=lambda x: abs(x["percent_change"]), reverse=True)


def identify_spending_anomalies(
    transactions: List[Transaction],
    num_days: int = 30,
    z_score_threshold: float = 2.0
) -> List[Dict[str, Any]]:
    """
    Identify recent spending anomalies using statistical methods.
    
    Args:
        transactions: List of Transaction objects
        num_days: Number of days to look back for recent transactions
        z_score_threshold: Z-score threshold for flagging anomalies
        
    Returns:
        List of dictionaries describing spending anomalies
    """
    # Convert transactions to DataFrame
    df = _transactions_to_dataframe(transactions)
    
    # Filter to only include expenses
    expense_df = df[df['transaction_type'] == 'expense']
    
    if expense_df.empty:
        return []
    
    # Define recent period
    latest_date = expense_df['transaction_date'].max()
    recent_start = latest_date - datetime.timedelta(days=num_days)
    
    # Split into historical and recent
    historical_df = expense_df[expense_df['transaction_date'] < recent_start]
    recent_df = expense_df[expense_df['transaction_date'] >= recent_start]
    
    # Need enough historical data for meaningful comparison
    if len(historical_df) < 10:
        return []
    
    anomalies = []
    
    # Check for daily spending anomalies
    # Group by date and calculate daily totals
    historical_daily = historical_df.groupby(
        historical_df['transaction_date'].dt.date
    )['amount'].sum()
    
    if len(historical_daily) >= 5:  # Need enough data points
        mean_daily = historical_daily.mean()
        std_daily = historical_daily.std()
        
        if std_daily > 0:  # Avoid division by zero
            # Check recent daily totals
            recent_daily = recent_df.groupby(
                recent_df['transaction_date'].dt.date
            )['amount'].sum()
            
            for date, amount in recent_daily.items():
                z_score = (amount - mean_daily) / std_daily
                
                if z_score > z_score_threshold:
                    anomalies.append({
                        "type": "daily",
                        "date": date.strftime("%Y-%m-%d"),
                        "amount": float(amount),
                        "average": float(mean_daily),
                        "z_score": z_score,
                        "transactions": len(recent_df[recent_df['transaction_date'].dt.date == date])
                    })
    
    # Check for category anomalies
    historical_category = historical_df.groupby('category')['amount'].agg(['mean', 'std'])
    
    for category in recent_df['category'].unique():
        if category in historical_category.index:
            mean_cat = historical_category.loc[category, 'mean']
            std_cat = historical_category.loc[category, 'std']
            
            if pd.notna(std_cat) and std_cat > 0:
                recent_cat_spending = recent_df[recent_df['category'] == category]['amount'].sum()
                
                # Normalize by time period
                days_in_historical = (historical_df['transaction_date'].max() - 
                                      historical_df['transaction_date'].min()).days
                
                if days_in_historical > 0:
                    daily_historical_avg = mean_cat * historical_df[
                        historical_df['category'] == category
                    ].groupby('transaction_date')['amount'].count().mean()
                    
                    expected_total = daily_historical_avg * num_days
                    
                    # Only compare if we have expected spending
                    if expected_total > 0:
                        ratio = recent_cat_spending / expected_total
                        
                        if ratio > 1 + (z_score_threshold * 0.5):  # Use a relaxed threshold for ratio
                            anomalies.append({
                                "type": "category",
                                "category": category,
                                "recent_total": float(recent_cat_spending),
                                "historical_avg": float(mean_cat),
                                "expected_total": float(expected_total),
                                "ratio": ratio,
                                "period": f"Last {num_days} days"
                            })
    
    return sorted(anomalies, key=lambda x: x.get("z_score", x.get("ratio", 0)), reverse=True)


def identify_weekend_vs_weekday_patterns(
    transactions: List[Transaction]
) -> Dict[str, Any]:
    """
    Analyze spending patterns between weekdays and weekends.
    
    Args:
        transactions: List of Transaction objects
        
    Returns:
        Dictionary with weekday vs weekend analysis
    """
    # Convert transactions to DataFrame
    df = _transactions_to_dataframe(transactions)
    
    # Filter to only include expenses
    expense_df = df[df['transaction_type'] == 'expense']
    
    if expense_df.empty:
        return {
            "weekday_avg": 0,
            "weekend_avg": 0,
            "weekday_total": 0,
            "weekend_total": 0,
            "weekend_categories": [],
            "weekday_categories": [],
            "weekend_percent": 0
        }
    
    # Add weekday/weekend flag
    expense_df['is_weekend'] = expense_df['transaction_date'].dt.dayofweek >= 5
    
    # Calculate statistics
    weekday_df = expense_df[~expense_df['is_weekend']]
    weekend_df = expense_df[expense_df['is_weekend']]
    
    # Get totals
    weekday_total = weekday_df['amount'].sum()
    weekend_total = weekend_df['amount'].sum()
    total_spending = weekday_total + weekend_total
    
    # Calculate percentages
    weekend_percent = (weekend_total / total_spending * 100) if total_spending > 0 else 0
    
    # Get number of days
    weekday_days = weekday_df['transaction_date'].dt.date.nunique()
    weekend_days = weekend_df['transaction_date'].dt.date.nunique()
    
    # Calculate daily averages (avoid division by zero)
    weekday_avg = weekday_total / weekday_days if weekday_days > 0 else 0
    weekend_avg = weekend_total / weekend_days if weekend_days > 0 else 0
    
    # Get top categories for each
    weekday_categories = weekday_df.groupby('category')['amount'].sum().sort_values(ascending=False)
    weekend_categories = weekend_df.groupby('category')['amount'].sum().sort_values(ascending=False)
    
    weekday_cat_list = [
        {"category": cat, "total": float(amount), "percent": float(amount / weekday_total * 100) if weekday_total > 0 else 0}
        for cat, amount in weekday_categories.head(5).items()
    ]
    
    weekend_cat_list = [
        {"category": cat, "total": float(amount), "percent": float(amount / weekend_total * 100) if weekend_total > 0 else 0}
        for cat, amount in weekend_categories.head(5).items()
    ]
    
    return {
        "weekday_avg": float(weekday_avg),
        "weekend_avg": float(weekend_avg),
        "weekday_total": float(weekday_total),
        "weekend_total": float(weekend_total),
        "weekend_categories": weekend_cat_list,
        "weekday_categories": weekday_cat_list,
        "weekend_percent": float(weekend_percent),
        "avg_ratio": float(weekend_avg / weekday_avg) if weekday_avg > 0 else 0
    }


def identify_end_of_month_pressure(
    transactions: List[Transaction],
    months_to_analyze: int = 6
) -> List[Dict[str, Any]]:
    """
    Analyze if spending increases toward the end of monthly pay cycles.
    
    Args:
        transactions: List of Transaction objects
        months_to_analyze: Number of months to analyze
        
    Returns:
        List of dictionaries with monthly end-of-month pressure analysis
    """
    # Convert transactions to DataFrame
    df = _transactions_to_dataframe(transactions)
    
    # Filter to only include expenses
    expense_df = df[df['transaction_type'] == 'expense']
    
    if expense_df.empty:
        return []
    
    # Get date range
    end_date = expense_df['transaction_date'].max().replace(hour=0, minute=0, second=0, microsecond=0)
    start_date = end_date - datetime.timedelta(days=30 * months_to_analyze)
    
    # Filter to desired time range
    expense_df = expense_df[
        (expense_df['transaction_date'] >= start_date) &
        (expense_df['transaction_date'] <= end_date)
    ]
    
    # Add month and day of month columns
    expense_df['year_month'] = expense_df['transaction_date'].dt.strftime('%Y-%m')
    expense_df['day_of_month'] = expense_df['transaction_date'].dt.day
    expense_df['days_in_month'] = expense_df['transaction_date'].apply(
        lambda x: calendar.monthrange(x.year, x.month)[1]
    )
    
    # Categorize days into parts of month (beginning, middle, end)
    def categorize_part_of_month(row):
        day = row['day_of_month']
        days_in_month = row['days_in_month']
        
        if day <= days_in_month / 3:
            return 'beginning'
        elif day <= 2 * days_in_month / 3:
            return 'middle'
        else:
            return 'end'
    
    expense_df['part_of_month'] = expense_df.apply(categorize_part_of_month, axis=1)
    
    # Analyze each month
    results = []
    for month in expense_df['year_month'].unique():
        month_df = expense_df[expense_df['year_month'] == month]
        
        # Need data from all parts of the month
        if not all(part in month_df['part_of_month'].values for part in ['beginning', 'middle', 'end']):
            continue
        
        # Calculate spending by part of month
        spending_by_part = month_df.groupby('part_of_month')['amount'].sum()
        
        # Calculate days in each part
        days_by_part = month_df.groupby('part_of_month')['transaction_date'].apply(
            lambda x: x.dt.date.nunique()
        )
        
        # Calculate daily average by part
        daily_avg = {}
        for part in ['beginning', 'middle', 'end']:
            if part in days_by_part and days_by_part[part] > 0:
                daily_avg[part] = spending_by_part.get(part, 0) / days_by_part[part]
            else:
                daily_avg[part] = 0
        
        # Check for end-of-month pressure
        if daily_avg['beginning'] > 0:
            end_to_beginning_ratio = daily_avg['end'] / daily_avg['beginning']
        else:
            end_to_beginning_ratio = 0
        
        # Calculate average day of month for transactions
        avg_day = (month_df['day_of_month'] * month_df['amount']).sum() / month_df['amount'].sum()
        
        results.append({
            "month": month,
            "beginning_spending": float(spending_by_part.get('beginning', 0)),
            "middle_spending": float(spending_by_part.get('middle', 0)),
            "end_spending": float(spending_by_part.get('end', 0)),
            "beginning_daily_avg": float(daily_avg['beginning']),
            "middle_daily_avg": float(daily_avg['middle']),
            "end_daily_avg": float(daily_avg['end']),
            "end_to_beginning_ratio": float(end_to_beginning_ratio),
            "has_end_month_pressure": end_to_beginning_ratio > 1.25,
            "avg_transaction_day": float(avg_day),
            "total_spending": float(month_df['amount'].sum())
        })
    
    # Sort by month
    return sorted(results, key=lambda x: x["month"])


def _transactions_to_dataframe(transactions: List[Transaction]) -> pd.DataFrame:
    """
    Convert a list of Transaction objects to a pandas DataFrame for analysis.
    
    Args:
        transactions: List of Transaction objects
    
    Returns:
        Pandas DataFrame with transaction data
    """
    if not transactions:
        # Return empty DataFrame with expected columns if no transactions
        return pd.DataFrame(columns=[
            'transaction_id', 'amount', 'category', 'description', 
            'transaction_date', 'transaction_type'
        ])
    
    data = []
    for transaction in transactions:
        try:
            # Make sure all required attributes exist
            transaction_data = {
                'transaction_id': getattr(transaction, 'transaction_id', None),
                'amount': float(getattr(transaction, 'amount', 0)),
                'category': getattr(transaction, 'category', 'Uncategorized'),
                'description': getattr(transaction, 'description', ''),
                'transaction_date': getattr(transaction, 'transaction_date', datetime.datetime.now().strftime('%Y-%m-%d')),
                'transaction_type': getattr(transaction, 'transaction_type', 'expense'),
            }
            data.append(transaction_data)
        except (AttributeError, ValueError, TypeError) as e:
            # Skip problematic transactions but log the issue
            print(f"Warning: Skipping transaction due to error: {e}")
            continue
    
    df = pd.DataFrame(data)
    
    # Ensure transaction_date is datetime
    if not df.empty:
        try:
            df['transaction_date'] = pd.to_datetime(df['transaction_date'])
        except (ValueError, TypeError):
            # If conversion fails, use current date
            df['transaction_date'] = datetime.datetime.now()
    
    return df


def _calculate_confidence_score(
    occurrences: int, 
    std_dev: float, 
    max_variance: float
) -> float:
    """Calculate confidence score for a recurring pattern."""
    # More occurrences and lower variance means higher confidence
    occurrence_factor = min(1.0, occurrences / 10)  # Max out at 10 occurrences
    variance_factor = 1.0 - min(1.0, std_dev / max_variance)
    
    # Weight both factors, with more emphasis on low variance
    return (occurrence_factor * 0.4) + (variance_factor * 0.6)


def _calculate_impulse_confidence(ratio: float, z_score: float) -> float:
    """Calculate confidence score for impulse purchase identification."""
    # Higher ratio to average and z-score means higher confidence
    ratio_factor = min(1.0, (ratio - 1.0) / 4.0)  # Normalize between 0-1
    z_score_factor = min(1.0, max(0, z_score / 5.0))  # Normalize between 0-1
    
    # Combine factors with weights
    return (ratio_factor * 0.6) + (z_score_factor * 0.4)