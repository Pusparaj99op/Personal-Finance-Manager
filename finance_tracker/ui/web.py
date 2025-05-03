"""
Web interface for the finance tracker application using Flask.
"""
from datetime import datetime, timedelta
from calendar import monthrange
import json

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, DateField, SelectField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, NumberRange, Optional

from finance_tracker.models.transaction import Transaction
from finance_tracker.models.category import Category
from finance_tracker.models.budget import Budget
from finance_tracker.storage.database import DatabaseStorage
from finance_tracker.analysis import trends
from finance_tracker.analysis import patterns
from finance_tracker.analysis import visualization
from finance_tracker.recommendations.budget_advisor import BudgetAdvisor
from finance_tracker.utils.helpers import format_currency

# Initialize Flask app
app = Flask(__name__, 
            template_folder='../../templates',
            static_folder='../../static')
app.secret_key = 'finance_tracker_secret_key'  # Change this in production

# Initialize database manager
db_manager = DatabaseStorage()

# Custom template filters
@app.template_filter('format_currency')
def template_format_currency(value):
    return format_currency(value)

@app.template_filter('format_date')
def template_format_date(date, format_string='%Y-%m-%d'):
    if isinstance(date, str):
        try:
            date = datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            return date
    return date.strftime(format_string)

# Forms
class TransactionForm(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
    amount = FloatField('Amount', validators=[DataRequired(), NumberRange(min=0.01)])
    transaction_date = DateField('Date', validators=[DataRequired()], default=datetime.today)
    transaction_type = SelectField('Transaction Type', 
                                   choices=[('expense', 'Expense'), ('income', 'Income')],
                                   validators=[DataRequired()])
    category = SelectField('Category', validators=[DataRequired()])
    notes = TextAreaField('Notes', validators=[Optional()])
    submit = SubmitField('Save Transaction')

class BudgetForm(FlaskForm):
    name = StringField('Budget Name', validators=[DataRequired()])
    start_date = DateField('Start Date', validators=[DataRequired()], default=datetime.today)
    end_date = DateField('End Date', validators=[DataRequired()], 
                         default=lambda: datetime.today() + timedelta(days=30))
    total_limit = FloatField('Total Budget Limit', validators=[Optional(), NumberRange(min=0)])
    submit = SubmitField('Save Budget')

class CategoryForm(FlaskForm):
    name = StringField('Category Name', validators=[DataRequired()])
    type = SelectField('Category Type', 
                       choices=[('expense', 'Expense'), ('income', 'Income')],
                       validators=[DataRequired()])
    submit = SubmitField('Save Category')

# Helper functions
def get_monthly_data(year=None, month=None):
    """Get financial data for a specific month"""
    today = datetime.today()
    year = year or today.year
    month = month or today.month
    
    # First and last day of the month
    first_day = datetime(year, month, 1)
    _, last_day_num = monthrange(year, month)
    last_day = datetime(year, month, last_day_num)
    
    # Get transactions for the month
    db_transactions = db_manager.get_all_transactions(
        start_date=first_day.strftime('%Y-%m-%d'),
        end_date=last_day.strftime('%Y-%m-%d')
    )
    
    # Calculate income, expenses, and balance
    total_income = sum(t['amount'] for t in db_transactions if t['transaction_type'] == 'income')
    total_expenses = sum(t['amount'] for t in db_transactions if t['transaction_type'] == 'expense')
    monthly_balance = total_income - total_expenses
    
    # Get spending by category
    expense_categories = {}
    for t in db_transactions:
        if t['transaction_type'] == 'expense':
            category = t.get('category', 'Uncategorized')
            if category not in expense_categories:
                expense_categories[category] = 0
            expense_categories[category] += t['amount']
    
    top_categories = sorted(expense_categories.items(), key=lambda x: x[1], reverse=True)
    
    # Get active budget and calculate progress
    budget = db_manager.get_active_budget()
    budget_vs_actual = []
    
    if budget:
        # Get budget limits by category
        cat_limits = budget.get_category_limits()
        
        # Calculate spending vs budget for each category
        for category, limit in cat_limits.items():
            spent = expense_categories.get(category, 0)
            budget_vs_actual.append({
                'category': category,
                'limit': limit,
                'spent': spent,
                'remaining': limit - spent if limit > 0 else 0,
                'percent': (spent / limit * 100) if limit > 0 else 0
            })
        
        # Sort by percentage spent
        budget_vs_actual.sort(key=lambda x: x['percent'], reverse=True)
    
    # Convert DB transactions to Transaction objects for analysis
    transactions = []
    for t in db_transactions:
        transaction = Transaction(
            transaction_id=t.get('transaction_id'),
            description=t.get('description', ''),
            amount=t.get('amount', 0),
            category=t.get('category', 'Uncategorized'),
            transaction_date=t.get('transaction_date', datetime.now().strftime('%Y-%m-%d')),
            transaction_type=t.get('transaction_type', 'expense')
        )
        transactions.append(transaction)
    
    # Get unusual expenses (impulse purchases that are higher than normal)
    unusual_expenses = patterns.identify_impulse_purchases(transactions)
    
    return {
        'transactions': db_transactions[:5],  # Just the most recent 5
        'total_income': total_income,
        'total_expenses': total_expenses,
        'monthly_balance': monthly_balance,
        'top_categories': top_categories,
        'budget': budget,
        'budget_vs_actual': budget_vs_actual,
        'unusual_expenses': unusual_expenses[:3] if unusual_expenses else []  # Top 3 unusual expenses
    }

# Routes
@app.route('/')
def index():
    """Home page / dashboard"""
    monthly_data = get_monthly_data()
    return render_template('dashboard.html', **monthly_data)

@app.route('/transactions', methods=['GET'])
def transactions():
    """Transactions list page"""
    # Get filter parameters
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    transaction_type = request.args.get('type')
    category = request.args.get('category')
    sort_by = request.args.get('sort', 'date')
    sort_dir = request.args.get('dir', 'desc')
    
    # Get transactions from database with filters
    transactions = db_manager.get_all_transactions(
        start_date=start_date,
        end_date=end_date,
        transaction_type=transaction_type,
        category=category
    )
    
    # Sort transactions
    if sort_by == 'date':
        transactions.sort(key=lambda x: x['transaction_date'], reverse=(sort_dir == 'desc'))
    elif sort_by == 'amount':
        transactions.sort(key=lambda x: x['amount'], reverse=(sort_dir == 'desc'))
    
    # Get categories for filter dropdown
    categories = db_manager.get_all_categories()
    
    # Calculate totals
    total_income = sum(t['amount'] for t in transactions if t['transaction_type'] == 'income')
    total_expenses = sum(t['amount'] for t in transactions if t['transaction_type'] == 'expense')
    net_amount = total_income - total_expenses
    
    return render_template('transactions.html',
                          transactions=transactions,
                          categories=categories,
                          total_income=total_income,
                          total_expenses=total_expenses,
                          net_amount=net_amount)

@app.route('/transactions/add', methods=['GET', 'POST'])
def add_transaction():
    """Add new transaction page"""
    # Get all categories for the dropdown
    categories = db_manager.get_all_categories()
    category_choices = [(c['name'], c['name']) for c in categories]
    
    # Create form and set category choices
    form = TransactionForm()
    form.category.choices = category_choices
    
    if form.validate_on_submit():
        # Create transaction object
        transaction = Transaction(
            description=form.description.data,
            amount=form.amount.data,
            transaction_date=form.transaction_date.data.strftime('%Y-%m-%d'),
            transaction_type=form.transaction_type.data,
            category=form.category.data,
            notes=form.notes.data
        )
        
        # Save to database
        db_manager.add_transaction(transaction)
        
        flash('Transaction added successfully!', 'success')
        return redirect(url_for('transactions'))
    
    return render_template('transaction_form.html', form=form, title='Add Transaction')

@app.route('/transactions/edit/<int:transaction_id>', methods=['GET', 'POST'])
def edit_transaction(transaction_id):
    """Edit transaction page"""
    # Get transaction from database
    transaction_data = db_manager.get_transaction(transaction_id)
    if not transaction_data:
        flash('Transaction not found', 'error')
        return redirect(url_for('transactions'))
    
    # Get all categories for the dropdown
    categories = db_manager.get_all_categories()
    category_choices = [(c['name'], c['name']) for c in categories]
    
    # Create form and set category choices
    form = TransactionForm()
    form.category.choices = category_choices
    
    if request.method == 'GET':
        # Populate form with existing data
        form.description.data = transaction_data['description']
        form.amount.data = transaction_data['amount']
        form.transaction_date.data = datetime.strptime(transaction_data['transaction_date'], '%Y-%m-%d')
        form.transaction_type.data = transaction_data['transaction_type']
        form.category.data = transaction_data['category']
        form.notes.data = transaction_data.get('notes', '')
    
    if form.validate_on_submit():
        # Update transaction data
        transaction = Transaction(
            id=transaction_id,
            description=form.description.data,
            amount=form.amount.data,
            transaction_date=form.transaction_date.data.strftime('%Y-%m-%d'),
            transaction_type=form.transaction_type.data,
            category=form.category.data,
            notes=form.notes.data
        )
        
        # Save to database
        db_manager.update_transaction(transaction)
        
        flash('Transaction updated successfully!', 'success')
        return redirect(url_for('transactions'))
    
    return render_template('transaction_form.html', form=form, title='Edit Transaction')

@app.route('/transactions/delete/<int:transaction_id>', methods=['POST'])
def delete_transaction(transaction_id):
    """Delete transaction"""
    db_manager.delete_transaction(transaction_id)
    flash('Transaction deleted successfully!', 'success')
    return redirect(url_for('transactions'))

@app.route('/budget', methods=['GET'])
def budget():
    """Budget overview page"""
    active_budget = db_manager.get_active_budget()
    
    if not active_budget:
        # Redirect to create budget page if no active budget
        return redirect(url_for('create_budget'))
    
    # Get budget data
    budget_data = active_budget.get_data()
    
    # Get all transactions in budget period
    transactions = db_manager.get_all_transactions(
        start_date=budget_data['start_date'],
        end_date=budget_data['end_date']
    )
    
    # Calculate spending by category
    spending_by_category = {}
    for t in transactions:
        if t['transaction_type'] == 'expense':
            category = t.get('category', 'Uncategorized')
            if category not in spending_by_category:
                spending_by_category[category] = 0
            spending_by_category[category] += t['amount']
    
    # Get category limits
    category_limits = active_budget.get_category_limits()
    
    # Compare actual spending vs budget
    budget_vs_actual = []
    for category, limit in category_limits.items():
        spent = spending_by_category.get(category, 0)
        budget_vs_actual.append({
            'category': category,
            'limit': limit,
            'spent': spent,
            'remaining': limit - spent if limit > 0 else 0,
            'percent': (spent / limit * 100) if limit > 0 else 0
        })
    
    # Add categories without explicit limits but with spending
    for category, spent in spending_by_category.items():
        if category not in category_limits:
            budget_vs_actual.append({
                'category': category,
                'limit': 0,
                'spent': spent,
                'remaining': 0,
                'percent': 100  # 100% over budget since there's no limit
            })
    
    # Sort by percentage spent
    budget_vs_actual.sort(key=lambda x: x['spent'], reverse=True)
    
    # Calculate total spent vs total limit
    total_spent = sum(spending_by_category.values())
    total_limit = budget_data.get('total_limit', 0)
    remaining = total_limit - total_spent if total_limit else 0
    
    budget_summary = {
        'name': budget_data['name'],
        'start_date': budget_data['start_date'],
        'end_date': budget_data['end_date'],
        'total_limit': total_limit,
        'total_spent': total_spent,
        'remaining': remaining,
        'percent': (total_spent / total_limit * 100) if total_limit > 0 else 0
    }
    
    return render_template('budget.html',
                          budget=budget_summary,
                          budget_vs_actual=budget_vs_actual)

@app.route('/budget/create', methods=['GET', 'POST'])
def create_budget():
    """Create budget page"""
    form = BudgetForm()
    
    # Get categories for category limits
    categories = db_manager.get_all_categories(category_type='expense')
    
    if form.validate_on_submit():
        # Create budget object
        budget = Budget(
            name=form.name.data,
            start_date=form.start_date.data.strftime('%Y-%m-%d'),
            end_date=form.end_date.data.strftime('%Y-%m-%d'),
            total_limit=form.total_limit.data if form.total_limit.data else 0
        )
        
        # Add category limits from form
        for category in categories:
            limit_field = f"category_{category['id']}"
            if limit_field in request.form and request.form[limit_field]:
                budget.add_category_limit(category['name'], float(request.form[limit_field]))
        
        # Save to database
        db_manager.add_budget(budget)
        
        flash('Budget created successfully!', 'success')
        return redirect(url_for('budget'))
    
    return render_template('budget_form.html', form=form, categories=categories)

@app.route('/categories', methods=['GET'])
def categories():
    """Categories management page"""
    category_objects = db_manager.get_all_categories()
    
    # Convert Category objects to dictionaries for the template
    categories = []
    for c in category_objects:
        categories.append({
            'category_id': c.category_id,
            'name': c.name,
            'type': c.category_type,
            'color': getattr(c, 'color', 'secondary'),
            'icon': getattr(c, 'icon', 'tag')
        })
    
    # Group by type
    expense_categories = [c for c in categories if c['type'] == 'expense']
    income_categories = [c for c in categories if c['type'] == 'income']
    
    return render_template('categories.html',
                          expense_categories=expense_categories,
                          income_categories=income_categories)

@app.route('/categories/add', methods=['GET', 'POST'])
def add_category():
    """Add category page"""
    form = CategoryForm()
    
    if form.validate_on_submit():
        # Create category object
        category = Category(
            name=form.name.data,
            category_type=form.type.data
        )
        
        # Save to database
        db_manager.add_category(category)
        
        flash('Category added successfully!', 'success')
        return redirect(url_for('categories'))
    
    return render_template('category_form.html', form=form, title='Add Category')

@app.route('/categories/edit/<int:category_id>', methods=['GET', 'POST'])
def edit_category(category_id):
    """Edit category page"""
    # Get category from database
    category_obj = db_manager.get_category(category_id)
    if not category_obj:
        flash('Category not found', 'error')
        return redirect(url_for('categories'))
    
    # Create form
    form = CategoryForm()
    
    if request.method == 'GET':
        # Populate form with existing data
        form.name.data = category_obj.name
        form.type.data = category_obj.category_type
    
    if form.validate_on_submit():
        # Update category data
        category_obj.name = form.name.data
        category_obj.category_type = form.type.data
        
        # Save to database
        db_manager.update_category(category_obj)
        
        flash('Category updated successfully!', 'success')
        return redirect(url_for('categories'))
    
    return render_template('category_form.html', form=form, title='Edit Category')

@app.route('/categories/delete/<int:category_id>', methods=['POST'])
def delete_category(category_id):
    """Delete category"""
    if db_manager.delete_category(category_id):
        flash('Category deleted successfully!', 'success')
    else:
        flash('Error deleting category', 'error')
    return redirect(url_for('categories'))

@app.route('/reports', methods=['GET'])
def reports():
    """Reports page"""
    report_type = request.args.get('type', 'spending')
    period = request.args.get('period', 'month')
    
    # Set date range based on period
    today = datetime.today()
    if period == 'month':
        start_date = datetime(today.year, today.month, 1)
        _, last_day = monthrange(today.year, today.month)
        end_date = datetime(today.year, today.month, last_day)
    elif period == 'year':
        start_date = datetime(today.year, 1, 1)
        end_date = datetime(today.year, 12, 31)
    else:  # Custom period
        start_date = datetime.strptime(request.args.get('start_date', today.strftime('%Y-%m-%d')), '%Y-%m-%d')
        end_date = datetime.strptime(request.args.get('end_date', today.strftime('%Y-%m-%d')), '%Y-%m-%d')
    
    # Get transactions for the period
    transactions = db_manager.get_all_transactions(
        start_date=start_date.strftime('%Y-%m-%d'),
        end_date=end_date.strftime('%Y-%m-%d')
    )
    
    # Generate report data based on type
    report_data = {}
    
    if report_type == 'spending':
        # Spending by category
        # Create a dictionary of spending by category
        category_spending = {}
        for t in transactions:
            if t['transaction_type'] == 'expense':
                category = t.get('category', 'Uncategorized')
                if category not in category_spending:
                    category_spending[category] = 0
                category_spending[category] += t['amount']
        
        report_data['spending_by_category'] = category_spending
        
        # Spending over time
        spending_over_time = trends.analyze_spending_trends(transactions)
        report_data['spending_over_time'] = spending_over_time
        
    elif report_type == 'income':
        # Income by category
        # Create a dictionary of income by category
        income_by_category = {}
        for t in transactions:
            if t['transaction_type'] == 'income':
                category = t.get('category', 'Uncategorized')
                if category not in income_by_category:
                    income_by_category[category] = 0
                income_by_category[category] += t['amount']
                
        report_data['income_by_category'] = income_by_category
        
        # Income over time - use transactions data directly since there's no specific income trends function
        income_trans = [t for t in transactions if t['transaction_type'] == 'income']
        income_over_time = trends.analyze_spending_trends(income_trans)
        report_data['income_over_time'] = income_over_time
        
    elif report_type == 'balance':
        # Income vs expenses over time - calculate from transactions
        expenses_data = trends.analyze_spending_trends(
            [t for t in transactions if t['transaction_type'] == 'expense']
        )
        income_data = trends.analyze_spending_trends(
            [t for t in transactions if t['transaction_type'] == 'income']
        )
        income_vs_expenses = {
            'expenses': expenses_data,
            'income': income_data
        }
        report_data['income_vs_expenses'] = income_vs_expenses
        
        # Net worth trend - using spending trends data as substitute
        all_trans_data = trends.analyze_spending_trends(transactions)
        report_data['net_worth_trend'] = all_trans_data
    
    return render_template('reports.html',
                          report_type=report_type,
                          period=period,
                          start_date=start_date,
                          end_date=end_date,
                          report_data=report_data)

@app.route('/recommendations', methods=['GET'])
def recommendations():
    """Budget recommendations page"""
    advisor = BudgetAdvisor(db_manager)
    
    # Get spending insights
    spending_insights = advisor.analyze_spending_patterns()
    
    # Get budget recommendations
    budget_recommendations = advisor.generate_budget_recommendations()
    
    # Get saving opportunities
    saving_opportunities = advisor.identify_saving_opportunities()
    
    return render_template('recommendations.html',
                          spending_insights=spending_insights,
                          budget_recommendations=budget_recommendations,
                          saving_opportunities=saving_opportunities)

@app.route('/api/transactions', methods=['GET'])
def api_transactions():
    """API endpoint for transactions data"""
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    transactions = db_manager.get_all_transactions(start_date=start_date, end_date=end_date)
    return jsonify(transactions)

@app.route('/api/spending-by-category', methods=['GET'])
def api_spending_by_category():
    """API endpoint for spending by category data"""
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    transactions = db_manager.get_all_transactions(
        start_date=start_date,
        end_date=end_date,
        transaction_type='expense'
    )
    
    # Group by category
    spending_by_category = {}
    for t in transactions:
        category = t.get('category', 'Uncategorized')
        if category not in spending_by_category:
            spending_by_category[category] = 0
        spending_by_category[category] += t['amount']
    
    # Convert to list of objects
    result = [{'category': cat, 'amount': amount} 
              for cat, amount in spending_by_category.items()]
    
    # Sort by amount
    result.sort(key=lambda x: x['amount'], reverse=True)
    
    return jsonify(result)

def run_app(host='0.0.0.0', port=5000, debug=True):
    """Run the Flask app"""
    app.run(host=host, port=port, debug=debug)


def main():
    """Main entry point for web interface"""
    # Set up database and initial data if needed
    print("Starting web interface on http://127.0.0.1:5000")
    print("Press CTRL+C to stop the server")
    
    # Run the Flask app
    run_app(host='127.0.0.1', port=5000, debug=True)


if __name__ == "__main__":
    main()