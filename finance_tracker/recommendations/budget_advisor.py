"""
Budget advisor module for generating personalized budget recommendations.
"""
from datetime import datetime, timedelta
from decimal import Decimal
from typing import List, Dict, Optional, Any, Tuple

from finance_tracker.models.transaction import Transaction
from finance_tracker.models.category import Category, DEFAULT_EXPENSE_CATEGORIES
from finance_tracker.models.budget import Budget
from finance_tracker.analysis.trends import (
    analyze_spending_trends,
    identify_unusual_expenses,
    analyze_recurring_expenses,
    forecast_monthly_expenses,
    calculate_category_allocations
)


class BudgetAdvisor:
    """
    Generates personalized budget recommendations based on spending patterns.
    """
    
    # Common financial rules
    SAVINGS_TARGET_PERCENT = 20  # 50/30/20 rule: 20% for savings
    NEEDS_TARGET_PERCENT = 50   # 50% for needs
    WANTS_TARGET_PERCENT = 30   # 30% for wants
    
    # Category classifications (simplified)
    NEEDS_CATEGORIES = {
        "Housing", "Utilities", "Groceries", "Transportation", 
        "Healthcare", "Insurance", "Education", "Debt Payments"
    }
    
    WANTS_CATEGORIES = {
        "Dining Out", "Entertainment", "Shopping", "Travel", 
        "Personal Care", "Hobbies", "Subscriptions"
    }
    
    SAVINGS_CATEGORIES = {
        "Savings", "Investments", "Emergency Fund", "Retirement"
    }
    
    def __init__(self, transactions: List[Transaction], categories: List[Category] = None):
        """
        Initialize the BudgetAdvisor.
        
        Args:
            transactions: List of Transaction objects to analyze
            categories: Optional list of Category objects with budget limits
        """
        self.transactions = transactions
        self.categories = categories or []
        
        # Extract income and expenses
        self.income_transactions = [t for t in transactions if t.is_income]
        self.expense_transactions = [t for t in transactions if t.is_expense]
        
        # Calculate basic financial metrics
        self._calculate_metrics()
    
    def _calculate_metrics(self) -> None:
        """Calculate basic financial metrics from transactions."""
        # Total income and expenses
        self.total_income = sum(t.amount for t in self.income_transactions)
        self.total_expenses = sum(t.amount for t in self.expense_transactions)
        
        # Monthly averages (based on last 6 months or available data)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=180)  # 6 months
        
        recent_income = [
            t for t in self.income_transactions 
            if t.transaction_date >= start_date
        ]
        recent_expenses = [
            t for t in self.expense_transactions 
            if t.transaction_date >= start_date
        ]
        
        date_range = []
        if recent_income:
            date_range.append(min(t.transaction_date for t in recent_income))
        if recent_expenses:
            date_range.append(min(t.transaction_date for t in recent_expenses))
        
        if date_range:
            earliest_date = min(date_range)
            months = max(1, (end_date - earliest_date).days / 30)
            self.avg_monthly_income = sum(t.amount for t in recent_income) / Decimal(months)
            self.avg_monthly_expenses = sum(t.amount for t in recent_expenses) / Decimal(months)
        else:
            self.avg_monthly_income = Decimal('0')
            self.avg_monthly_expenses = Decimal('0')
        
        # Savings rate
        if self.total_income > 0:
            self.savings_rate = (self.total_income - self.total_expenses) / self.total_income * 100
        else:
            self.savings_rate = Decimal('0')
        
        # Categorize spending
        self.spending_by_category = {}
        for transaction in self.expense_transactions:
            if transaction.category in self.spending_by_category:
                self.spending_by_category[transaction.category] += transaction.amount
            else:
                self.spending_by_category[transaction.category] = transaction.amount
    
    def get_budget_health_summary(self) -> Dict[str, Any]:
        """
        Generate an overall summary of budget health.
        
        Returns:
            Dictionary with budget health metrics
        """
        # Analyze spending distribution
        needs_spending = self._calculate_spending_type_total("needs")
        wants_spending = self._calculate_spending_type_total("wants")
        savings_amount = self.total_income - self.total_expenses
        
        # Calculate percentages of income
        if self.total_income > 0:
            needs_percent = (needs_spending / self.total_income) * 100
            wants_percent = (wants_spending / self.total_income) * 100
            savings_percent = (savings_amount / self.total_income) * 100
        else:
            needs_percent = Decimal('0')
            wants_percent = Decimal('0')
            savings_percent = Decimal('0')
        
        # Determine overall health score (0-100)
        health_score = self._calculate_health_score(needs_percent, wants_percent, savings_percent)
        
        # Get status for each area
        needs_status = "good" if needs_percent <= self.NEEDS_TARGET_PERCENT else "high"
        wants_status = "good" if wants_percent <= self.WANTS_TARGET_PERCENT else "high"
        savings_status = "good" if savings_percent >= self.SAVINGS_TARGET_PERCENT else "low"
        
        # Create health summary
        return {
            "overall_score": health_score,
            "status_description": self._get_health_description(health_score),
            "savings_rate": savings_percent,
            "needs_percent": needs_percent,
            "wants_percent": wants_percent,
            "savings_percent": savings_percent,
            "needs_status": needs_status,
            "wants_status": wants_status,
            "savings_status": savings_status,
            "monthly_surplus": self.avg_monthly_income - self.avg_monthly_expenses,
            "has_budget_deficit": self.total_expenses > self.total_income
        }
    
    def _calculate_spending_type_total(self, spending_type: str) -> Decimal:
        """
        Calculate total spending for a given type (needs/wants/savings).
        
        Args:
            spending_type: One of "needs", "wants", or "savings"
        
        Returns:
            Total amount spent in the given category type
        """
        target_categories = set()
        
        if spending_type == "needs":
            target_categories = self.NEEDS_CATEGORIES
        elif spending_type == "wants":
            target_categories = self.WANTS_CATEGORIES
        elif spending_type == "savings":
            target_categories = self.SAVINGS_CATEGORIES
        
        total = Decimal('0')
        for category, amount in self.spending_by_category.items():
            if category in target_categories:
                total += amount
        
        return total
    
    def _calculate_health_score(
        self, needs_percent: Decimal, wants_percent: Decimal, savings_percent: Decimal
    ) -> int:
        """
        Calculate an overall budget health score (0-100).
        
        Args:
            needs_percent: Percentage of income spent on needs
            wants_percent: Percentage of income spent on wants
            savings_percent: Percentage of income saved
        
        Returns:
            Health score between 0 and 100
        """
        # Start with a perfect score and subtract for deviations from targets
        score = 100
        
        # Penalize for spending too much on needs
        if needs_percent > self.NEEDS_TARGET_PERCENT:
            penalty = min(30, (needs_percent - self.NEEDS_TARGET_PERCENT) * 1.5)
            score -= penalty
        
        # Penalize for spending too much on wants
        if wants_percent > self.WANTS_TARGET_PERCENT:
            penalty = min(30, (wants_percent - self.WANTS_TARGET_PERCENT) * 2)
            score -= penalty
        
        # Penalize for not saving enough
        if savings_percent < self.SAVINGS_TARGET_PERCENT:
            penalty = min(40, (self.SAVINGS_TARGET_PERCENT - savings_percent) * 2)
            score -= penalty
        
        # Ensure score is between 0 and 100
        return max(0, min(100, int(score)))
    
    def _get_health_description(self, health_score: int) -> str:
        """
        Get a description of budget health based on score.
        
        Args:
            health_score: Budget health score (0-100)
        
        Returns:
            Description of budget health
        """
        if health_score >= 90:
            return "Excellent"
        elif health_score >= 80:
            return "Very Good"
        elif health_score >= 70:
            return "Good"
        elif health_score >= 60:
            return "Fair"
        elif health_score >= 50:
            return "Needs Improvement"
        elif health_score >= 40:
            return "Concerning"
        elif health_score >= 30:
            return "Poor"
        else:
            return "Critical"
    
    def generate_budget_recommendation(self) -> Dict[str, Any]:
        """
        Generate a comprehensive budget recommendation.
        
        Returns:
            Dictionary with budget recommendations
        """
        # Get health summary for context
        health_summary = self.get_budget_health_summary()
        
        # Calculate recommended spending by category based on 50/30/20 rule
        recommended_budget = self._generate_recommended_budget()
        
        # Get spending trends and insights
        trends = analyze_spending_trends(self.transactions)
        unusual_expenses = identify_unusual_expenses(self.transactions)
        recurring_expenses = analyze_recurring_expenses(self.transactions)
        forecast = forecast_monthly_expenses(self.transactions)
        
        # Generate savings opportunities
        savings_opportunities = self._identify_savings_opportunities()
        
        # Generate action items based on overall budget health
        action_items = self._generate_action_items(health_summary, trends)
        
        return {
            "health_summary": health_summary,
            "recommended_budget": recommended_budget,
            "savings_opportunities": savings_opportunities,
            "action_items": action_items,
            "trends": trends,
            "unusual_expenses": unusual_expenses,
            "recurring_expenses": recurring_expenses,
            "forecast": forecast
        }
    
    def _generate_recommended_budget(self) -> Dict[str, Decimal]:
        """
        Generate recommended monthly budget by category.
        
        Returns:
            Dictionary mapping category names to recommended monthly amounts
        """
        if self.avg_monthly_income <= 0:
            return {}
        
        # Get actual spending allocations (percentages)
        actual_allocations = calculate_category_allocations(self.transactions)
        
        # Get category breakdowns from actual spending
        needs_categories = {}
        wants_categories = {}
        savings_categories = {}
        other_categories = {}
        
        for category, percentage in actual_allocations.items():
            if category in self.NEEDS_CATEGORIES:
                needs_categories[category] = percentage
            elif category in self.WANTS_CATEGORIES:
                wants_categories[category] = percentage
            elif category in self.SAVINGS_CATEGORIES:
                savings_categories[category] = percentage
            else:
                other_categories[category] = percentage
        
        # Apply 50/30/20 rule to income
        target_needs = self.avg_monthly_income * Decimal(str(self.NEEDS_TARGET_PERCENT / 100))
        target_wants = self.avg_monthly_income * Decimal(str(self.WANTS_TARGET_PERCENT / 100))
        target_savings = self.avg_monthly_income * Decimal(str(self.SAVINGS_TARGET_PERCENT / 100))
        
        # Distribute budgets across categories while maintaining relative proportions
        recommended_budget = {}
        
        # Handle needs categories
        self._allocate_category_budgets(
            needs_categories, target_needs, recommended_budget
        )
        
        # Handle wants categories
        self._allocate_category_budgets(
            wants_categories, target_wants, recommended_budget
        )
        
        # Handle savings categories
        if savings_categories:
            self._allocate_category_budgets(
                savings_categories, target_savings, recommended_budget
            )
        else:
            # If no savings categories, recommend a generic one
            recommended_budget["Savings"] = target_savings
        
        # Handle other categories by fitting them into needs or wants
        if other_categories:
            # Decide whether to put "other" categories in needs or wants based on available budget
            needs_used = sum(amount for cat, amount in recommended_budget.items() 
                           if cat in self.NEEDS_CATEGORIES)
            needs_remaining = target_needs - needs_used
            
            wants_used = sum(amount for cat, amount in recommended_budget.items() 
                           if cat in self.WANTS_CATEGORIES)
            wants_remaining = target_wants - wants_used
            
            # Allocate to whichever has more room
            if needs_remaining > wants_remaining:
                self._allocate_category_budgets(
                    other_categories, needs_remaining, recommended_budget
                )
            else:
                self._allocate_category_budgets(
                    other_categories, wants_remaining, recommended_budget
                )
        
        return recommended_budget
    
    def _allocate_category_budgets(
        self,
        category_percentages: Dict[str, float],
        total_budget: Decimal,
        result_dict: Dict[str, Decimal]
    ) -> None:
        """
        Allocate a budget amount across categories based on relative percentages.
        
        Args:
            category_percentages: Dictionary mapping categories to percentages
            total_budget: Total budget to allocate
            result_dict: Dictionary to update with allocations
        """
        # If no categories, return without changes
        if not category_percentages:
            return
        
        # Calculate total percentage
        total_percent = sum(category_percentages.values())
        
        if total_percent > 0:
            # Allocate proportionally to each category
            for category, percentage in category_percentages.items():
                allocation = (percentage / total_percent) * total_budget
                result_dict[category] = allocation
        else:
            # If no percentage data, divide equally
            equal_share = total_budget / len(category_percentages)
            for category in category_percentages:
                result_dict[category] = equal_share
    
    def _identify_savings_opportunities(self) -> List[Dict[str, Any]]:
        """
        Identify potential savings opportunities.
        
        Returns:
            List of dictionaries with savings opportunities
        """
        opportunities = []
        
        # Find categories where spending is significantly higher than average
        if self.spending_by_category:
            # Calculate average spending per category
            avg_category_spending = sum(self.spending_by_category.values()) / len(self.spending_by_category)
            
            # Look for categories with above-average spending
            for category, amount in self.spending_by_category.items():
                if amount > avg_category_spending * Decimal('1.5') and category in self.WANTS_CATEGORIES:
                    opportunities.append({
                        "category": category,
                        "amount": amount,
                        "average": avg_category_spending,
                        "potential_savings": amount - avg_category_spending,
                        "description": f"Consider reducing spending on {category}. "
                                      f"You're spending {amount / avg_category_spending:.1f}x "
                                      f"the average amount in this category."
                    })
        
        # Check for high savings potential if we have budget deficit
        if self.total_expenses > self.total_income:
            deficit = self.total_expenses - self.total_income
            opportunities.append({
                "category": "Overall Budget",
                "amount": deficit,
                "potential_savings": deficit,
                "description": f"You're spending more than your income by {deficit}. "
                              f"Consider reducing expenses or increasing income to balance your budget."
            })
        
        return opportunities
    
    def _generate_action_items(
        self, health_summary: Dict[str, Any], trends: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Generate personalized action items based on budget health.
        
        Args:
            health_summary: Budget health summary
            trends: Spending trends analysis
        
        Returns:
            List of action items with descriptions and priorities
        """
        action_items = []
        
        # Check for deficit spending
        if health_summary["has_budget_deficit"]:
            action_items.append({
                "title": "Balance your budget",
                "description": "You're spending more than you earn. Focus on reducing expenses or increasing income.",
                "priority": "high"
            })
        
        # Check savings rate
        if health_summary["savings_rate"] < self.SAVINGS_TARGET_PERCENT:
            action_items.append({
                "title": "Increase your savings rate",
                "description": f"Your current savings rate is {health_summary['savings_rate']:.1f}%. "
                              f"Aim for at least {self.SAVINGS_TARGET_PERCENT}% of income.",
                "priority": "high" if health_summary["savings_rate"] < 10 else "medium"
            })
        
        # Check spending distribution
        if health_summary["wants_percent"] > self.WANTS_TARGET_PERCENT:
            action_items.append({
                "title": "Reduce discretionary spending",
                "description": f"You're spending {health_summary['wants_percent']:.1f}% of income on wants, "
                              f"which exceeds the recommended {self.WANTS_TARGET_PERCENT}%.",
                "priority": "medium"
            })
        
        # Check spending trends
        if trends["spending_trend"] == "increasing":
            action_items.append({
                "title": "Monitor increasing expenses",
                "description": "Your spending has been trending upward. Review recent increases to ensure they align with your goals.",
                "priority": "medium"
            })
        
        # If spending is high in specific categories, suggest reviews
        top_categories = trends.get("top_categories", [])
        if top_categories and len(top_categories) > 0:
            top_category, top_amount = top_categories[0]
            action_items.append({
                "title": f"Review {top_category} spending",
                "description": f"Your highest expense category is {top_category} at {top_amount}. "
                              f"Look for potential savings in this area.",
                "priority": "medium"
            })
        
        # If too few actions, recommend general financial health items
        if len(action_items) < 3:
            if "Emergency Fund" not in self.spending_by_category:
                action_items.append({
                    "title": "Build an emergency fund",
                    "description": "Consider setting aside 3-6 months of expenses in an emergency fund for financial security.",
                    "priority": "medium"
                })
            
            action_items.append({
                "title": "Review recurring subscriptions",
                "description": "Regularly audit your recurring expenses and cancel unused subscriptions.",
                "priority": "low"
            })
        
        # Always recommend tracking expenses
        action_items.append({
            "title": "Maintain regular expense tracking",
            "description": "Continue tracking all expenses to maintain awareness of your spending habits.",
            "priority": "low"
        })
        
        return action_items
    
    def create_monthly_budget(self) -> Budget:
        """
        Create a recommended monthly budget based on analysis.
        
        Returns:
            A Budget object with recommended limits
        """
        # Generate recommended budget allocation
        recommended_amounts = self._generate_recommended_budget()
        
        # Set budget period for the upcoming month
        today = datetime.now()
        start_date = datetime(today.year, today.month, 1)
        # Move to the next month
        if today.month == 12:
            end_date = datetime(today.year + 1, 1, 1)
        else:
            end_date = datetime(today.year, today.month + 1, 1)
        # Subtract one day to get the last day of the current month
        end_date = end_date - timedelta(days=1)
        
        # Create the budget
        budget = Budget(
            name=f"Recommended Budget for {today.strftime('%B %Y')}",
            start_date=start_date,
            end_date=end_date,
            category_limits=recommended_amounts,
            total_limit=self.avg_monthly_income
        )
        
        return budget