"""
Command-line interface for the finance tracker application.
"""
import sys
import os
import cmd
import datetime
from decimal import Decimal
from typing import List, Dict, Optional, Any

from finance_tracker.models.transaction import Transaction
from finance_tracker.models.category import Category, create_default_categories
from finance_tracker.models.budget import Budget
from finance_tracker.storage.database import DatabaseStorage
from finance_tracker.analysis.trends import (
    analyze_spending_trends,
    identify_unusual_expenses,
    analyze_recurring_expenses
)
from finance_tracker.recommendations.budget_advisor import BudgetAdvisor


class FinanceTrackerCLI(cmd.Cmd):
    """
    Command-line interface for the finance tracker application.
    """
    intro = """
    =============================================
      Personal Finance Tracker - Command Line
    =============================================
    Type 'help' or '?' to list commands.
    Type 'exit' or 'quit' to exit.
    """
    prompt = "finance> "
    
    def __init__(self, db_path: str = 'finance_tracker.db'):
        super().__init__()
        self.db = DatabaseStorage(db_path)
        self.current_budget = None
        # Try to load active budget
        self.load_active_budget()
    
    def load_active_budget(self):
        """Load the active budget if one exists."""
        self.current_budget = self.db.get_active_budget()
        if self.current_budget:
            print(f"Loaded active budget: {self.current_budget.name}")
    
    def do_add_transaction(self, arg):
        """
        Add a new transaction.
        Usage: add_transaction
        """
        print("\n=== Add New Transaction ===")
        
        # Ask for transaction type
        while True:
            tx_type = input("Transaction type (expense/income) [expense]: ").lower() or "expense"
            if tx_type in ["expense", "income"]:
                break
            print("Invalid type. Please enter 'expense' or 'income'.")
        
        # Get amount
        while True:
            amount_str = input("Amount: ")
            try:
                amount = Decimal(amount_str)
                if amount <= 0:
                    print("Amount must be positive.")
                    continue
                break
            except:
                print("Invalid amount. Please enter a valid number.")
        
        # Get category
        categories = self.db.get_all_categories(tx_type)
        print("\nAvailable Categories:")
        for i, category in enumerate(categories, 1):
            print(f"{i}. {category.name}")
        print(f"{len(categories) + 1}. Add new category")
        
        while True:
            cat_choice = input(f"Category (1-{len(categories) + 1}): ")
            try:
                choice_num = int(cat_choice)
                if 1 <= choice_num <= len(categories):
                    selected_category = categories[choice_num - 1].name
                    break
                elif choice_num == len(categories) + 1:
                    # Add new category
                    new_cat_name = input("New category name: ")
                    new_cat = Category(name=new_cat_name, category_type=tx_type)
                    self.db.add_category(new_cat)
                    selected_category = new_cat_name
                    break
                else:
                    print(f"Please enter a number between 1 and {len(categories) + 1}")
            except:
                print("Invalid choice. Please enter a number.")
        
        # Get description
        description = input("Description: ")
        
        # Get date
        while True:
            date_str = input("Date (YYYY-MM-DD) [today]: ") or datetime.datetime.now().strftime("%Y-%m-%d")
            try:
                tx_date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
                break
            except:
                print("Invalid date format. Please use YYYY-MM-DD.")
        
        # Create and save the transaction
        transaction = Transaction(
            amount=amount,
            category=selected_category,
            description=description,
            transaction_date=tx_date,
            transaction_type=tx_type
        )
        
        tx_id = self.db.add_transaction(transaction)
        print(f"\nTransaction added successfully (ID: {tx_id})")
        
        # Check if this would exceed budget
        if self.current_budget and tx_type == "expense" and selected_category in self.current_budget.category_limits:
            category_limit = self.current_budget.category_limits[selected_category]
            start_date = self.current_budget.start_date
            end_date = self.current_budget.end_date
            
            # Get total spent in this category during budget period
            transactions = self.db.get_all_transactions(
                start_date=start_date,
                end_date=end_date,
                category=selected_category,
                transaction_type="expense"
            )
            
            total_spent = sum(t.amount for t in transactions)
            
            if total_spent > category_limit:
                print(f"\nWARNING: This transaction puts you over budget for {selected_category}!")
                print(f"Budget: ${category_limit:.2f}, Spent: ${total_spent:.2f}")
    
    def do_list_transactions(self, arg):
        """
        List recent transactions.
        Usage: list_transactions [num=10]
        """
        try:
            num = int(arg) if arg else 10
        except:
            num = 10
        
        transactions = self.db.get_all_transactions()[:num]
        
        if not transactions:
            print("No transactions found.")
            return
        
        print("\n=== Recent Transactions ===")
        print(f"{'ID':>4} {'Date':<10} {'Type':<8} {'Category':<15} {'Amount':>10} {'Description':<30}")
        print("-" * 80)
        
        for tx in transactions:
            sign = "-" if tx.is_expense else "+"
            print(f"{tx.transaction_id:>4} {tx.transaction_date.strftime('%Y-%m-%d')} "
                  f"{tx.transaction_type:<8} {tx.category:<15} "
                  f"{sign}${tx.amount:>9.2f} {tx.description[:30]:<30}")
    
    def do_create_budget(self, arg):
        """
        Create a new budget.
        Usage: create_budget
        """
        print("\n=== Create New Budget ===")
        
        # Get budget name
        name = input("Budget name: ")
        
        # Get date range
        while True:
            start_date_str = input("Start date (YYYY-MM-DD) [1st of current month]: ") or datetime.datetime.now().replace(day=1).strftime("%Y-%m-%d")
            try:
                start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d")
                break
            except:
                print("Invalid date format. Please use YYYY-MM-DD.")
        
        while True:
            # Default to last day of month
            last_day = (start_date.replace(month=start_date.month % 12 + 1, day=1) if start_date.month < 12 
                      else start_date.replace(year=start_date.year + 1, month=1, day=1)) - datetime.timedelta(days=1)
            end_date_str = input(f"End date (YYYY-MM-DD) [{last_day.strftime('%Y-%m-%d')}]: ") or last_day.strftime("%Y-%m-%d")
            try:
                end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d")
                if end_date <= start_date:
                    print("End date must be after start date.")
                    continue
                break
            except:
                print("Invalid date format. Please use YYYY-MM-DD.")
        
        # Get total budget limit (optional)
        total_limit = None
        limit_str = input("Total budget limit (optional): ")
        if limit_str:
            try:
                total_limit = Decimal(limit_str)
            except:
                print("Invalid amount. Total limit will not be set.")
        
        # Get category limits
        category_limits = {}
        categories = self.db.get_all_categories("expense")
        
        print("\nSet limits for expense categories (leave blank for no limit):")
        for category in categories:
            limit_str = input(f"{category.name}: ")
            if limit_str:
                try:
                    limit = Decimal(limit_str)
                    category_limits[category.name] = limit
                except:
                    print(f"Invalid amount for {category.name}. No limit will be set.")
        
        # Create and save the budget
        budget = Budget(
            name=name,
            start_date=start_date,
            end_date=end_date,
            category_limits=category_limits,
            total_limit=total_limit
        )
        
        budget_id = self.db.add_budget(budget)
        self.current_budget = budget
        print(f"\nBudget created successfully (ID: {budget_id})")
    
    def do_show_budget(self, arg):
        """
        Show current budget and status.
        Usage: show_budget
        """
        if not self.current_budget:
            print("No active budget found. Use 'create_budget' to create one.")
            return
        
        budget = self.current_budget
        print(f"\n=== Budget: {budget.name} ===")
        print(f"Period: {budget.start_date.strftime('%Y-%m-%d')} to {budget.end_date.strftime('%Y-%m-%d')}")
        
        if budget.total_limit:
            print(f"Total Limit: ${budget.total_limit:.2f}")
        
        # Get actual spending in budget period
        txs = self.db.get_all_transactions(
            start_date=budget.start_date,
            end_date=budget.end_date,
            transaction_type="expense"
        )
        
        # Group by category
        category_spending = {}
        for tx in txs:
            if tx.category in category_spending:
                category_spending[tx.category] += tx.amount
            else:
                category_spending[tx.category] = tx.amount
        
        # Calculate total spent
        total_spent = sum(category_spending.values())
        
        # Print status
        print(f"\n{'Category':<20} {'Budget':>10} {'Spent':>10} {'Remaining':>10} {'%':>6}")
        print("-" * 60)
        
        for category, limit in budget.category_limits.items():
            spent = category_spending.get(category, Decimal('0'))
            remaining = limit - spent
            percent = (spent / limit * 100) if limit > 0 else 0
            
            status = "✓" if spent <= limit else "✗"
            
            print(f"{category:<20} ${limit:>9.2f} ${spent:>9.2f} ${remaining:>9.2f} {percent:>5.1f}% {status}")
        
        # Print categories without limits
        other_categories = set(category_spending.keys()) - set(budget.category_limits.keys())
        if other_categories:
            print("\nCategories without budget limits:")
            for category in other_categories:
                spent = category_spending.get(category, Decimal('0'))
                print(f"{category:<20} {'N/A':>10} ${spent:>9.2f}")
        
        # Print overall status
        if budget.total_limit:
            print(f"\nOverall Budget: ${budget.total_limit:.2f}")
            print(f"Total Spent:    ${total_spent:.2f}")
            remaining = budget.total_limit - total_spent
            print(f"Remaining:      ${remaining:.2f}")
            
            percent_used = (total_spent / budget.total_limit * 100) if budget.total_limit > 0 else 0
            print(f"Budget used:    {percent_used:.1f}%")
    
    def do_analyze_spending(self, arg):
        """
        Analyze spending patterns.
        Usage: analyze_spending [months=6]
        """
        try:
            months = int(arg) if arg else 6
        except:
            months = 6
        
        print(f"\n=== Spending Analysis (Last {months} Months) ===")
        
        # Get transactions for the period
        end_date = datetime.datetime.now()
        start_date = end_date - datetime.timedelta(days=30 * months)
        
        transactions = self.db.get_all_transactions(
            start_date=start_date,
            end_date=end_date
        )
        
        if not transactions:
            print("No transactions found for the selected period.")
            return
        
        # Get spending trends
        trends = analyze_spending_trends(transactions, period_months=months)
        
        # Print summary
        print(f"\nTotal Spending: ${trends['total_spending']:.2f}")
        print(f"Average Monthly: ${trends['avg_monthly_spending']:.2f}")
        print(f"Spending Trend: {trends['spending_trend'].capitalize()}")
        
        if trends['month_over_month_change'] != Decimal('0'):
            change_str = f"{trends['month_over_month_change']:+.1f}%" 
            print(f"Month-over-month change: {change_str}")
        
        # Print top categories
        print("\nTop Spending Categories:")
        for i, (category, amount) in enumerate(trends['top_categories'], 1):
            print(f"{i}. {category}: ${amount:.2f}")
        
        # Print insights
        if trends['highest_spending_day']:
            print(f"\nHighest Spending Day: {trends['highest_spending_day']}")
        
        if trends['highest_spending_month']:
            print(f"Highest Spending Month: {trends['highest_spending_month']}")
        
        # Get unusual expenses
        unusual = identify_unusual_expenses(transactions)
        if unusual:
            print("\nUnusual Expenses:")
            for tx in unusual[:5]:  # Show top 5
                print(f"- {tx.description}: ${tx.amount:.2f} on {tx.transaction_date.strftime('%Y-%m-%d')}")
        
        # Get recurring expenses
        recurring = analyze_recurring_expenses(transactions)
        if recurring['monthly'] or recurring['weekly']:
            print("\nRecurring Expenses:")
            
            if recurring['monthly']:
                print("Monthly:")
                for exp in recurring['monthly'][:3]:  # Show top 3
                    print(f"- {exp['description']}: ${exp['avg_amount']:.2f}")
            
            if recurring['weekly']:
                print("Weekly:")
                for exp in recurring['weekly'][:3]:  # Show top 3
                    print(f"- {exp['description']}: ${exp['avg_amount']:.2f}")
    
    def do_get_recommendations(self, arg):
        """
        Get personalized budget recommendations.
        Usage: get_recommendations
        """
        print("\n=== Personal Budget Recommendations ===")
        
        # Get all transactions
        transactions = self.db.get_all_transactions()
        
        if not transactions:
            print("Not enough transaction data for recommendations.")
            return
        
        # Get all categories
        categories = self.db.get_all_categories()
        
        # Create budget advisor
        advisor = BudgetAdvisor(transactions, categories)
        recommendations = advisor.generate_budget_recommendation()
        
        # Print health summary
        health = recommendations["health_summary"]
        print(f"\nBudget Health Score: {health['overall_score']}/100 ({health['status_description']})")
        
        if health["has_budget_deficit"]:
            print("⚠️ Budget Deficit: You're spending more than you earn.")
        
        print(f"\nSpending Distribution:")
        print(f"Needs:   {health['needs_percent']:.1f}% (Target: {advisor.NEEDS_TARGET_PERCENT}%)")
        print(f"Wants:   {health['wants_percent']:.1f}% (Target: {advisor.WANTS_TARGET_PERCENT}%)")
        print(f"Savings: {health['savings_percent']:.1f}% (Target: {advisor.SAVINGS_TARGET_PERCENT}%)")
        
        # Print action items
        print("\nRecommended Actions:")
        for i, action in enumerate(recommendations["action_items"], 1):
            priority_marker = "‼️" if action["priority"] == "high" else "❗" if action["priority"] == "medium" else "ℹ️"
            print(f"{i}. {priority_marker} {action['title']}")
            print(f"   {action['description']}")
        
        # Print savings opportunities
        if recommendations["savings_opportunities"]:
            print("\nPotential Savings Opportunities:")
            for i, opportunity in enumerate(recommendations["savings_opportunities"], 1):
                print(f"{i}. {opportunity['category']}: ${opportunity['potential_savings']:.2f}")
                print(f"   {opportunity['description']}")
        
        # Ask if user wants to create a recommended budget
        create_budget = input("\nWould you like to create a recommended budget? (y/n) [n]: ").lower() == 'y'
        if create_budget:
            budget = advisor.create_monthly_budget()
            budget_id = self.db.add_budget(budget)
            self.current_budget = budget
            print(f"\nRecommended budget created successfully (ID: {budget_id})")
            print("Use 'show_budget' to see details.")
    
    def do_exit(self, arg):
        """Exit the program."""
        print("Thank you for using Personal Finance Tracker!")
        return True
    
    def do_quit(self, arg):
        """Exit the program."""
        return self.do_exit(arg)
    
    def default(self, line):
        """Handle unknown command."""
        print(f"Unknown command: {line}")
        print("Type 'help' or '?' to list available commands.")


def main():
    """Run the CLI application."""
    # Get database path
    db_path = os.environ.get('FINANCE_DB_PATH', 'finance_tracker.db')
    
    # Start the CLI
    cli = FinanceTrackerCLI(db_path)
    try:
        cli.cmdloop()
    except KeyboardInterrupt:
        print("\nExiting due to user interrupt...")
    except Exception as e:
        print(f"An error occurred: {e}")
        raise


if __name__ == '__main__':
    main()