# Personal Finance Manager - Documentation

This document provides detailed information on how to use the Personal Finance Manager application, including setup, usage instructions, and technical details.

## Table of Contents

1. [System Overview](#system-overview)
2. [Installation](#installation)
3. [Command Line Interface](#command-line-interface)
4. [Web Interface](#web-interface)
5. [Data Management](#data-management)
6. [Analysis Features](#analysis-features)
7. [Budget System](#budget-system)
8. [Recommendation Engine](#recommendation-engine)
9. [Technical Architecture](#technical-architecture)
10. [Development Guide](#development-guide)

## System Overview

The Personal Finance Manager is a comprehensive financial management application designed to help users track expenses, analyze spending patterns, create budgets, and receive personalized financial recommendations. The system employs a modular architecture with separate components handling distinct responsibilities like data modeling, storage, analysis, visualization, and user interface presentation.

## Installation

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Standard Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Pusparaj99op/Personal-Finance-Manager.git
   cd Personal-Finance-Manager
   ```

2. Create a virtual environment:
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Database Configuration

The application uses SQLite as its database by default. When you first run the application, it will create a database file named `finance_tracker.db` in the application directory.

If you want to specify a different database path:
```bash
python main.py --db-path /path/to/your/database.db
```

## Command Line Interface

The CLI provides a text-based interface for all application features.

### Starting the CLI

```bash
python main.py
# or explicitly
python main.py --interface cli
```

### Available Commands

#### Managing Transactions

- **Adding a transaction**:
  ```
  finance> add_transaction
  ```
  This will prompt you for:
  - Transaction type (expense/income)
  - Amount
  - Category
  - Description
  - Date (defaults to today)

- **Listing transactions**:
  ```
  finance> list_transactions
  # or specify how many to list
  finance> list_transactions 20
  ```

#### Budget Management

- **Creating a budget**:
  ```
  finance> create_budget
  ```
  This will guide you through:
  - Setting a budget name
  - Defining start and end dates
  - Setting an optional total limit
  - Setting category-specific limits

- **Viewing budget status**:
  ```
  finance> show_budget
  ```
  Displays:
  - Budget period
  - Total and category-specific limits
  - Actual spending against limits
  - Percentage of budget used
  - Warnings for categories exceeding limits

#### Analysis and Recommendations

- **Analyzing spending patterns**:
  ```
  finance> analyze_spending
  # or specify analysis period in months
  finance> analyze_spending 12
  ```
  Shows:
  - Total and average monthly spending
  - Month-over-month change
  - Spending trend (increasing/decreasing/fluctuating)
  - Top spending categories
  - Unusual expenses
  - Recurring expenses (weekly/monthly)

- **Getting financial recommendations**:
  ```
  finance> get_recommendations
  ```
  Provides:
  - Financial health assessment
  - Distribution across needs/wants/savings
  - Prioritized action items
  - Savings opportunities
  - Option to create a recommended budget

#### Other Commands

- **Exit the application**:
  ```
  finance> exit
  # or
  finance> quit
  ```

## Web Interface

The web interface provides a visual way to interact with the application through your browser.

### Starting the Web Server

```bash
python main.py --interface web
```

This will start a Flask web server. Open your browser and go to `http://localhost:5000` to access the interface.

### Web Interface Sections

#### Dashboard

The home page displays:
- Summary of your financial situation
- Recent transactions
- Budget status
- Spending distribution by category
- Income vs. expenses chart
- Spending trends over time

#### Transactions Management

- **View all transactions**: Navigate to the Transactions page
- **Add new transaction**: Click "Add Transaction" button
- **Edit transaction**: Click the edit icon next to any transaction
- **Delete transaction**: Click the delete icon next to any transaction

#### Budget Management

- **View budgets**: Navigate to the Budget page
- **Create new budget**: Click "Create Budget" button
- **View budget details**: Click on any budget name
- **Track budget progress**: View visual progress bars on the budget page

#### Financial Analysis

- **View analysis**: Navigate to the Analysis page
- **Change analysis period**: Use the date selector
- **View different charts**: Toggle between chart types
- **See recommendations**: Navigate to the Recommendations page

## Data Management

### Transaction Data

Each transaction includes:
- Transaction ID (automatically assigned)
- Amount (stored as Decimal for financial accuracy)
- Category
- Description
- Transaction Date
- Transaction Type (expense/income)

### Categories

The application organizes transactions into categories. Default categories include:
- Expense categories: Food, Housing, Transportation, Entertainment, etc.
- Income categories: Salary, Freelance, Investments, etc.

You can add custom categories as needed.

### Budgets

Budgets have the following attributes:
- Name
- Start and End dates
- Total limit (optional)
- Category-specific limits (optional)

## Analysis Features

### Spending Trends Analysis

The trends analysis module provides:

- **Total spending** over a configurable period
- **Average monthly spending**
- **Month-over-month change** with percentage
- **Spending trend** classification (increasing/decreasing/fluctuating)
- **Top spending categories** with amounts
- **Highest spending day** of week
- **Highest spending month**

### Unusual Expenses Detection

The application identifies expenses that are significantly higher than the category average (by default, 2x the average). This helps you spot one-time large purchases or potential issues.

### Recurring Expenses Detection

The system automatically identifies patterns in your spending to detect:
- Weekly recurring expenses
- Monthly recurring expenses
- Other periodic expenses

### Expense Forecasting

Based on your historical data, the system forecasts:
- Expected expenses for future months
- Growth or decline trends in spending

## Budget System

### Creating Budgets

Budgets can be created for any time period (monthly, yearly, etc.) with:
- Overall spending limit
- Individual category limits

### Budget Tracking

The application tracks:
- Current spending against budget limits
- Percentage of budget used
- Remaining amounts
- Visual indicators for budget status

### Budget Alerts

The system provides warnings when:
- Adding a transaction that would exceed a category limit
- Approaching overall budget limits

## Recommendation Engine

### Financial Health Assessment

The application assesses your financial health based on:
- Income vs. expense ratio
- Distribution across needs, wants, and savings
- Adherence to the 50/30/20 rule

### Personalized Recommendations

Based on your spending patterns, the system provides:
- Prioritized action items to improve financial health
- Potential areas for saving money
- Budget adjustment suggestions

### Smart Budget Creation

The recommendation engine can create a personalized budget based on:
- Your historical spending patterns
- Financial best practices
- Your income level

## Technical Architecture

### Component Structure

The application uses a modular design with these key components:

1. **Models**: Core data structures defining the domain objects
   - `Transaction`: Represents financial transactions
   - `Category`: Manages classification system
   - `Budget`: Handles budget planning and limits

2. **Storage**: Database interaction layer
   - `DatabaseStorage`: SQLite implementation for persistence
   - `Export`: Handles data import/export

3. **Analysis**: Data processing components
   - `Trends`: Analyzes spending patterns over time
   - `Patterns`: Detects recurring expenses and anomalies
   - `Visualization`: Creates charts and graphical representations

4. **Recommendations**: Financial advice system
   - `BudgetAdvisor`: Generates personalized financial recommendations

5. **UI**: User interface implementations
   - `CLI`: Command-line interface
   - `Web`: Flask-based web interface

6. **Utils**: Support utilities
   - `Config`: Configuration management
   - `Helpers`: General utility functions

### Data Flow

1. User inputs transaction data through the UI layer
2. Data is validated and saved via the Storage layer
3. Analysis layer processes the data to extract insights
4. Recommendation layer uses analysis results to generate advice
5. UI layer presents information back to the user

## Development Guide

### Project Setup for Development

1. Fork and clone the repository
2. Create virtual environment and install dependencies
   ```bash
   pip install -r requirements.txt
   ```
3. Run tests
   ```bash
   python -m unittest discover -s finance_tracker/tests
   ```

### Architecture Decisions

- **SQLite Database**: Chosen for simplicity, portability, and zero configuration
- **Flask**: Lightweight web framework that's easy to extend
- **Pandas/NumPy**: Powerful data analysis and manipulation tools
- **Matplotlib**: Flexible visualization library for creating charts
- **Modular Design**: Components are separated to enable easy extension and testing

### Extending the Application

#### Adding a New Analysis Feature

1. Create a new function in the appropriate analysis module
2. Update the UI to expose the functionality
3. Add appropriate tests

#### Creating a New Visualization

1. Add a new function in `visualization.py`
2. Initialize and display in the appropriate UI module
3. Add corresponding CSS/JS for web interface if needed

#### Adding New Recommendation Types

1. Extend the `budget_advisor.py` module with new recommendation logic
2. Update the UI to display the new recommendations
3. Add tests for the new functionality

---

## Appendix

### Database Schema

```
transactions
- transaction_id (INTEGER PRIMARY KEY)
- amount (DECIMAL)
- category (TEXT)
- description (TEXT)
- transaction_date (DATE)
- transaction_type (TEXT)

categories
- category_id (INTEGER PRIMARY KEY)
- name (TEXT)
- type (TEXT)

budgets
- budget_id (INTEGER PRIMARY KEY)
- name (TEXT)
- start_date (DATE)
- end_date (DATE)
- total_limit (DECIMAL)
- category_limits (TEXT, JSON)
```

### Configuration Options

The application's behavior can be modified through the `config.py` module:

- Database settings (path, backup directory)
- Analysis parameters (period, thresholds)
- Budget recommendation targets (needs/wants/savings percentages)
- Visualization settings (chart styles, colors)

### Error Codes and Troubleshooting

Common issues and solutions:

1. **Database errors**
   - Ensure the database path is writable
   - Check for file permissions issues

2. **Import errors**
   - Verify all dependencies are installed
   - Check virtual environment activation

3. **Visualization issues**
   - Ensure matplotlib backend is compatible with your system
   - For web interface, check browser console for JavaScript errors