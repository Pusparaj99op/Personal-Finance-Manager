"""
Visualization module for the finance tracker application.
"""
from datetime import datetime, timedelta
import calendar
from typing import List, Dict, Optional, Tuple, Any, Union
from decimal import Decimal

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
from matplotlib.figure import Figure


def plot_spending_by_category(category_spending: Dict[str, Decimal]) -> Figure:
    """
    Create a pie chart showing spending by category.
    
    Args:
        category_spending: Dictionary mapping category names to spent amounts
    
    Returns:
        Matplotlib figure object
    """
    # Sort categories by spending amount (descending)
    sorted_categories = sorted(
        category_spending.items(), 
        key=lambda x: x[1], 
        reverse=True
    )
    
    # Extract categories and amounts
    categories = [item[0] for item in sorted_categories]
    amounts = [float(item[1]) for item in sorted_categories]
    
    # If there are too many categories, group the smallest ones into "Other"
    MAX_CATEGORIES = 8
    if len(categories) > MAX_CATEGORIES:
        other_amount = sum(amounts[MAX_CATEGORIES-1:])
        categories = categories[:MAX_CATEGORIES-1] + ["Other"]
        amounts = amounts[:MAX_CATEGORIES-1] + [other_amount]
    
    # Create pie chart
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.pie(
        amounts, 
        labels=categories,
        autopct='%1.1f%%',
        startangle=90,
        shadow=False,
    )
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
    plt.title("Spending by Category", fontsize=16)
    
    return fig


def plot_monthly_spending_trend(monthly_data: Dict[str, Decimal], months_to_show: int = 12) -> Figure:
    """
    Create a line chart showing spending trends over months.
    
    Args:
        monthly_data: Dictionary mapping month strings (YYYY-MM) to total spent amounts
        months_to_show: Number of months to display
    
    Returns:
        Matplotlib figure object
    """
    # Convert dictionary to sorted list of tuples
    data_points = sorted(monthly_data.items())[-months_to_show:]
    
    # Extract months and amounts
    months = [item[0] for item in data_points]
    amounts = [float(item[1]) for item in data_points]
    
    # Convert month strings to datetime objects for better x-axis formatting
    month_dates = [datetime.strptime(month, "%Y-%m") for month in months]
    
    # Create line chart
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(month_dates, amounts, marker='o', linestyle='-', linewidth=2, markersize=8)
    
    # Format x-axis to show month and year
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    plt.xticks(rotation=45)
    
    # Add grid and labels
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.set_xlabel('Month', fontsize=12)
    ax.set_ylabel('Amount Spent', fontsize=12)
    plt.title('Monthly Spending Trend', fontsize=16)
    
    # Add data values above points
    for i, amount in enumerate(amounts):
        ax.annotate(
            f"${amount:.2f}", 
            (month_dates[i], amount),
            textcoords="offset points",
            xytext=(0, 10),
            ha='center'
        )
    
    plt.tight_layout()
    return fig


def plot_income_vs_expenses(
    monthly_income: Dict[str, Decimal],
    monthly_expenses: Dict[str, Decimal],
    months_to_show: int = 12
) -> Figure:
    """
    Create a bar chart comparing income vs expenses over months.
    
    Args:
        monthly_income: Dictionary mapping month strings to income amounts
        monthly_expenses: Dictionary mapping month strings to expense amounts
        months_to_show: Number of months to display
    
    Returns:
        Matplotlib figure object
    """
    # Get union of all months from both dictionaries
    all_months = sorted(set(monthly_income) | set(monthly_expenses))[-months_to_show:]
    
    # Prepare data
    months_datetime = [datetime.strptime(month, "%Y-%m") for month in all_months]
    income_values = [float(monthly_income.get(month, Decimal('0'))) for month in all_months]
    expense_values = [float(monthly_expenses.get(month, Decimal('0'))) for month in all_months]
    
    # Set up bar chart
    fig, ax = plt.subplots(figsize=(12, 6))
    bar_width = 0.35
    index = np.arange(len(all_months))
    
    # Create bars
    income_bars = ax.bar(
        index - bar_width/2, 
        income_values, 
        bar_width, 
        label='Income',
        color='green',
        alpha=0.7
    )
    expense_bars = ax.bar(
        index + bar_width/2, 
        expense_values, 
        bar_width, 
        label='Expenses',
        color='red',
        alpha=0.7
    )
    
    # Add labels and formatting
    ax.set_xlabel('Month', fontsize=12)
    ax.set_ylabel('Amount', fontsize=12)
    ax.set_title('Monthly Income vs. Expenses', fontsize=16)
    ax.set_xticks(index)
    ax.set_xticklabels([date.strftime('%b %Y') for date in months_datetime], rotation=45)
    ax.legend()
    
    # Add grid
    ax.grid(True, linestyle='--', axis='y', alpha=0.7)
    
    # Add data labels on bars
    def add_labels(bars):
        for bar in bars:
            height = bar.get_height()
            ax.annotate(
                f"${height:.0f}",
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3),  # 3 points vertical offset
                textcoords="offset points",
                ha='center',
                va='bottom',
                fontsize=8
            )
    
    add_labels(income_bars)
    add_labels(expense_bars)
    
    plt.tight_layout()
    return fig


def plot_budget_progress(
    budget_limits: Dict[str, Decimal],
    actual_spending: Dict[str, Decimal]
) -> Figure:
    """
    Create a horizontal bar chart comparing budget limits to actual spending.
    
    Args:
        budget_limits: Dictionary mapping category names to budget limits
        actual_spending: Dictionary mapping category names to actual spent amounts
    
    Returns:
        Matplotlib figure object
    """
    # Get categories that appear in either dictionary
    categories = sorted(set(budget_limits) | set(actual_spending))
    
    # Prepare data
    limits = [float(budget_limits.get(cat, Decimal('0'))) for cat in categories]
    spending = [float(actual_spending.get(cat, Decimal('0'))) for cat in categories]
    
    # Calculate percentages for display
    percentages = []
    for i, cat in enumerate(categories):
        if cat in budget_limits and float(budget_limits[cat]) > 0:
            spent = float(actual_spending.get(cat, Decimal('0')))
            budget = float(budget_limits[cat])
            percentages.append(f"{(spent / budget * 100):.1f}%")
        else:
            percentages.append("N/A")
    
    # Create horizontal bar chart
    fig, ax = plt.subplots(figsize=(10, max(6, len(categories) * 0.5)))
    
    # Plot bars
    y_pos = np.arange(len(categories))
    ax.barh(y_pos - 0.2, limits, 0.4, label='Budget', color='blue', alpha=0.6)
    ax.barh(y_pos + 0.2, spending, 0.4, label='Actual', color='red', alpha=0.6)
    
    # Add labels and formatting
    ax.set_yticks(y_pos)
    ax.set_yticklabels(categories)
    ax.invert_yaxis()  # Labels read top-to-bottom
    ax.set_xlabel('Amount')
    ax.set_title('Budget vs. Actual Spending by Category')
    ax.legend()
    
    # Add percentage labels
    for i, (lim, spent, pct) in enumerate(zip(limits, spending, percentages)):
        # Add budget amount
        ax.text(
            lim + max(limits) * 0.02,
            i - 0.2,
            f"${lim:.2f}",
            va='center',
            fontsize=8
        )
        # Add actual amount and percentage
        ax.text(
            spent + max(limits) * 0.02,
            i + 0.2,
            f"${spent:.2f} ({pct})",
            va='center',
            fontsize=8
        )
    
    plt.tight_layout()
    return fig


def plot_spending_heatmap(
    transactions_by_day: Dict[Tuple[int, int], Decimal],
    year: Optional[int] = None
) -> Figure:
    """
    Create a heatmap showing spending patterns by day of week and month.
    
    Args:
        transactions_by_day: Dictionary mapping (month, day) tuples to amounts
        year: Optional year to filter data for
    
    Returns:
        Matplotlib figure object
    """
    # Initialize data array for heatmap: [month, day_of_week]
    data = np.zeros((12, 7))
    
    # Fill the data array
    for (month, day), amount in transactions_by_day.items():
        # Convert to 0-based indices
        month_idx = month - 1  # Months are 1-12
        
        # Calculate day of week (0 = Monday, 6 = Sunday)
        # This assumes the day is from the current or specified year
        target_year = year or datetime.now().year
        date = datetime(target_year, month, day)
        day_of_week = date.weekday()
        
        data[month_idx, day_of_week] += float(amount)
    
    # Create heatmap
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Plot the heatmap
    im = ax.imshow(data, cmap='YlOrRd')
    
    # Add colorbar
    cbar = fig.colorbar(im, ax=ax, label='Amount Spent')
    
    # Set labels
    month_names = [calendar.month_abbr[i] for i in range(1, 13)]
    day_names = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    
    ax.set_xticks(np.arange(len(day_names)))
    ax.set_yticks(np.arange(len(month_names)))
    ax.set_xticklabels(day_names)
    ax.set_yticklabels(month_names)
    
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
    
    # Add title
    year_text = f" in {year}" if year else ""
    plt.title(f"Spending Heatmap by Day of Week and Month{year_text}")
    
    # Loop over data dimensions and create text annotations
    for i in range(len(month_names)):
        for j in range(len(day_names)):
            if data[i, j] > 0:
                ax.text(j, i, f"${data[i, j]:.0f}", 
                        ha="center", va="center", 
                        color="black" if data[i, j] < np.max(data)/2 else "white",
                        fontsize=8)
    
    plt.tight_layout()
    return fig