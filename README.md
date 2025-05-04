# 💰 Personal Finance Manager

<div align="center">

![Finance Banner](https://img.shields.io/badge/Personal-Finance%20Manager-2ea44f?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCIgd2lkdGg9IjI0IiBoZWlnaHQ9IjI0IiBmaWxsPSJ3aGl0ZSI+PHBhdGggZD0iTTEyIDJDNi40OCAyIDIgNi40OCAyIDEyczQuNDggMTAgMTAgMTAgMTAtNC40OCAxMC0xMFMxNy41MiAyIDEyIDJ6bTAgMThjLTQuNDEgMC04LTMuNTktOC04czMuNTktOCA4LTggOCAzLjU5IDggOC0zLjU5IDgtOCA4em0tLjUtMTFWN2gxdjJoMVY3aDJ2MmgtLjkyYy40OS44Mi43OTIgMS44MTMuODIgM2gtLjAxYy0uMDM2IDEuNTY4LS41OTggMy4wOC0xLjU5NCA0LjA5NEMxMy40MiAxNy4wOCAxMS45MDcgMTcuNjQgMTAuMzQgMTcuNjk5Yy0xLjU2OC4wNi0zLjEwNy0uMzgzLTQuMzM0LTEuMjVsLjY4OC0uNzgxYzEuMDgyLjczIDIuMzYzIDEuMDkgMy42NTYgMS4wM2E1LjE5NyA1LjE5NyAwIDAgMCAzLjMxMy0xLjM0M2MuODE0LS44MTMgMS4yNy0xLjkxOSAxLjI3Ni0zLjA3LS4wMDQtLjk1Mi0uMzEyLTEuODc5LS44NzUtMi42MjVsLS4xNy0uMjVoMS4yMDdWOUgxMS41eiIvPjwvc3ZnPg==)
[![GitHub License](https://img.shields.io/github/license/Pusparaj99op/Personal-Finance-Manager?style=for-the-badge&color=blue)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.7+-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org)
![SQLite](https://img.shields.io/badge/sqlite-0B84CE?style=for-the-badge&logo=sqlite&logoColor=white)

**A modern, comprehensive financial management solution for tracking expenses, creating budgets, and achieving financial goals.**

[Key Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Screenshots](#-screenshots) • [Contributing](#-contributing)

</div>

## ✨ Features

<table>
  <tr>
    <td width="50%">
      <h3>Financial Management</h3>
      <ul>
        <li>✅ Track expenses and income</li>
        <li>✅ Categorize transactions automatically</li>
        <li>✅ Store data securely in SQLite database</li>
        <li>✅ Detect recurring expenses</li>
      </ul>
    </td>
    <td width="50%">
      <h3>Budget Planning</h3>
      <ul>
        <li>✅ Create custom budgets by category</li>
        <li>✅ Track budget progress visually</li>
        <li>✅ Get alerts for budget overruns</li>
        <li>✅ Personalized budget recommendations</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td>
      <h3>Analysis Tools</h3>
      <ul>
        <li>✅ Visualize spending patterns</li>
        <li>✅ Analyze historical trends</li>
        <li>✅ Identify unusual expenses</li>
        <li>✅ Financial health scoring</li>
      </ul>
    </td>
    <td>
      <h3>User Interface</h3>
      <ul>
        <li>✅ Command Line Interface</li>
        <li>✅ Interactive Web Dashboard</li>
        <li>✅ Responsive design</li>
        <li>✅ Data visualization charts</li>
      </ul>
    </td>
  </tr>
</table>

## 📦 Installation

### Prerequisites
- Python 3.7+
- pip package manager

### Setup Steps

1. **Clone the repository**

   ```bash
   git clone https://github.com/Pusparaj99op/Personal-Finance-Manager.git
   cd Personal-Finance-Manager
   ```

2. **Create virtual environment**

   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Usage

### Command Line Interface (CLI)

The fastest way to start tracking your finances:

```bash
python main.py
```

or explicitly specify the CLI interface:

```bash
python main.py --interface cli
```

#### CLI Commands

| Command | Description |
|---------|-------------|
| `add_transaction` | Add a new expense or income transaction |
| `list_transactions [num]` | List recent transactions (default: 10) |
| `create_budget` | Create a new budget |
| `show_budget` | Show current budget and status |
| `analyze_spending [months]` | Analyze spending patterns (default: 6 months) |
| `get_recommendations` | Get personalized budget recommendations |
| `exit` or `quit` | Exit the application |

### Web Interface

For a more visual experience, run with the web interface:

```bash
python main.py --interface web
```

Then open your browser and navigate to `http://localhost:5000`

<div align="center">
<img src="https://via.placeholder.com/800x450.png?text=Finance+Tracker+Web+Interface" alt="Web Interface Preview" width="80%">
</div>

#### Web Interface Features

- 📊 Interactive dashboard with financial summaries
- 📝 Intuitive transaction management
- 💸 Visual budget tracking
- 📈 Interactive spending charts
- 💡 Smart financial recommendations
- 📱 Mobile-responsive design

### Command Line Arguments

```bash
python main.py --db-path /path/to/database.db --interface cli
```

| Option | Description |
|--------|-------------|
| `--interface`, `-i` | Interface to use (`cli`, `gui`, or `web`) |
| `--db-path` | Path to the database file |

## 🧩 How It Works

### Core Components

#### 1. Transaction Management
The application allows you to record both expense and income transactions with detailed categorization. Every transaction includes:
- Amount
- Category
- Description
- Date
- Transaction type (income/expense)

#### 2. Budget System
Set up comprehensive budgets to monitor your spending:
- Create budgets for specific time periods
- Set overall spending limits
- Configure individual category limits
- Get visual representations of budget progress
- Receive alerts when approaching or exceeding limits

#### 3. Analysis Engine
The analysis module provides insights into your financial behavior:
- Spending trend analysis over configurable time periods
- Identification of unusual expenses that exceed category averages
- Automatic detection of recurring expenses (weekly, monthly)
- Forecasting of future expenses based on historical patterns
- Visualization through charts and graphs

#### 4. Recommendation System
Get personalized financial advice:
- Smart budget suggestions based on spending history
- Financial health scoring using the 50/30/20 rule (needs/wants/savings)
- Identification of potential savings opportunities
- Actionable recommendations prioritized by impact

## 🏗️ Project Structure

```
finance_tracker/
├── models/             # Core data models (Transaction, Category, Budget)
│   ├── transaction.py  # Transaction data model
│   ├── category.py     # Category classification system
│   └── budget.py       # Budget planning system
├── storage/            # Data persistence
│   ├── database.py     # SQLite database operations
│   └── export.py       # Data import/export functionality
├── analysis/           # Data analysis and visualization
│   ├── trends.py       # Spending trend analysis
│   ├── patterns.py     # Pattern identification
│   └── visualization.py # Charts and graphs generation
├── recommendations/    # Budgeting recommendations
│   └── budget_advisor.py # Budget suggestion algorithms
├── ui/                 # User interface implementations
│   ├── cli.py          # Command-line interface
│   └── web.py          # Flask-based web interface
└── utils/              # Helper utilities
    ├── config.py       # Configuration management
    └── helpers.py      # Common utilities
static/                 # Web assets (CSS, JS, images)
templates/              # HTML templates for web interface
```

## 🛠️ Technologies Used

<div align="center">

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-%23ffffff.svg?style=for-the-badge&logo=Matplotlib&logoColor=black)
![Bootstrap](https://img.shields.io/badge/bootstrap-%238511FA.svg?style=for-the-badge&logo=bootstrap&logoColor=white)

</div>

## 🚀 Getting Started with Development

### Setting Up Development Environment

1. **Fork and clone the repository**

2. **Install development dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Database initialization**
   The application will automatically create and initialize the database on first run.

4. **Run tests**
   ```bash
   python -m unittest discover -s finance_tracker/tests
   ```

### Architecture Overview

This application follows a modular design pattern:

1. **Data Models Layer**: Defines the core domain objects
2. **Storage Layer**: Handles persistence and retrieval operations
3. **Analysis Layer**: Processes financial data to extract insights
4. **Recommendation Layer**: Generates advice based on analysis
5. **UI Layer**: Presents information and collects user input

## 📸 Screenshots

<div align="center">
<table>
  <tr>
    <td><img src="https://via.placeholder.com/400x225.png?text=Dashboard" alt="Dashboard"/></td>
    <td><img src="https://via.placeholder.com/400x225.png?text=Transactions" alt="Transactions"/></td>
  </tr>
  <tr>
    <td><img src="https://via.placeholder.com/400x225.png?text=Budget+Tracking" alt="Budget Tracking"/></td>
    <td><img src="https://via.placeholder.com/400x225.png?text=Analysis" alt="Analysis"/></td>
  </tr>
</table>
</div>

## 🚀 Future Enhancements

- 🖥️ Native GUI interface
- 📊 Advanced data analytics
- ☁️ Cloud synchronization
- 📱 Mobile companion app
- 💱 Multi-currency support
- 📈 Investment portfolio tracking
- 🎯 Financial goal setting and tracking
- 🔒 Enhanced security features

## 👥 Contributing

Contributions make the open-source community amazing! Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📦 Dependencies

- **Flask**: Web framework for the browser interface
- **Matplotlib**: Data visualization library for generating charts
- **NumPy**: Numerical operations for analysis
- **Pandas**: Data analysis and manipulation
- **SQLite**: Embedded database for data storage

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.

## 🙏 Acknowledgments

- Financial planning best practices based on the 50/30/20 budgeting rule
- Inspired by various personal finance management tools
- Icons and badges from [Shields.io](https://shields.io)

---

<div align="center">
Made with ❤️ by <a href="https://github.com/Pusparaj99op">Pusparaj</a>
</div>