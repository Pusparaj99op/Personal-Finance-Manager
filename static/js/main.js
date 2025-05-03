// Main JavaScript for Finance Tracker

document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap tooltips
    var tooltips = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltips.map(function (tooltip) {
        return new bootstrap.Tooltip(tooltip);
    });

    // Initialize Bootstrap popovers
    var popovers = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popovers.map(function (popover) {
        return new bootstrap.Popover(popover);
    });
    
    // Transaction type toggle in add/edit transaction form
    const transactionTypeRadios = document.querySelectorAll('input[name="type"]');
    if (transactionTypeRadios.length) {
        transactionTypeRadios.forEach(radio => {
            radio.addEventListener('change', function() {
                toggleCategorySelect(this.value);
            });
        });
        
        // Initial toggle based on selected type
        const selectedType = document.querySelector('input[name="type"]:checked');
        if (selectedType) {
            toggleCategorySelect(selectedType.value);
        }
    }
    
    // Date range picker initialization
    const dateRangeInputs = document.querySelectorAll('.date-range-picker');
    if (dateRangeInputs.length) {
        dateRangeInputs.forEach(input => {
            // This would normally use a date picker library like daterangepicker.js
            // For simplicity, we're just using the HTML5 date inputs
            input.addEventListener('change', function() {
                const relatedForm = this.closest('form');
                if (relatedForm && relatedForm.dataset.autoSubmit === 'true') {
                    relatedForm.submit();
                }
            });
        });
    }
    
    // Auto-submit forms with class 'auto-submit' when select changes
    const autoSubmitSelects = document.querySelectorAll('form.auto-submit select');
    if (autoSubmitSelects.length) {
        autoSubmitSelects.forEach(select => {
            select.addEventListener('change', function() {
                this.closest('form').submit();
            });
        });
    }
    
    // Initialize any charts
    initializeCharts();
    
    // Handle modals for delete confirmation
    setupDeleteConfirmation();
});

// Toggle category select based on transaction type
function toggleCategorySelect(type) {
    const expenseCategories = document.getElementById('expense-categories');
    const incomeCategories = document.getElementById('income-categories');
    
    if (!expenseCategories || !incomeCategories) return;
    
    if (type === 'expense') {
        expenseCategories.classList.remove('d-none');
        incomeCategories.classList.add('d-none');
    } else {
        incomeCategories.classList.remove('d-none');
        expenseCategories.classList.add('d-none');
    }
}

// Setup delete confirmation
function setupDeleteConfirmation() {
    const deleteModal = document.getElementById('deleteConfirmationModal');
    if (!deleteModal) return;
    
    deleteModal.addEventListener('show.bs.modal', function (event) {
        // Button that triggered the modal
        const button = event.relatedTarget;
        
        // Extract info from data-bs-* attributes
        const itemId = button.getAttribute('data-bs-id');
        const itemName = button.getAttribute('data-bs-name');
        const formAction = button.getAttribute('data-bs-action');
        
        // Update the modal's content
        const modalTitle = deleteModal.querySelector('.modal-title');
        const modalBody = deleteModal.querySelector('.modal-body p');
        const modalForm = deleteModal.querySelector('form');
        
        modalTitle.textContent = `Delete ${itemName}`;
        modalBody.textContent = `Are you sure you want to delete this ${itemName.toLowerCase()}? This action cannot be undone.`;
        modalForm.action = formAction;
    });
}

// Initialize dashboard charts
function initializeCharts() {
    initializeSpendingChart();
    initializeBudgetChart();
    initializeIncomeExpenseChart();
    initializeTrendChart();
}

// Initialize spending by category chart
function initializeSpendingChart() {
    const spendingChartEl = document.getElementById('spending-chart');
    if (!spendingChartEl) return;
    
    // Check if we have data from the template
    if (!window.chartData || !window.chartData.spending) return;
    
    const data = window.chartData.spending;
    
    new Chart(spendingChartEl, {
        type: 'doughnut',
        data: {
            labels: data.labels,
            datasets: [{
                data: data.values,
                backgroundColor: data.colors || [
                    '#0d6efd', '#6610f2', '#6f42c1', '#d63384', 
                    '#dc3545', '#fd7e14', '#ffc107', '#198754', 
                    '#20c997', '#0dcaf0', '#6c757d'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'right',
                }
            },
        }
    });
}

// Initialize budget usage chart
function initializeBudgetChart() {
    const budgetChartEl = document.getElementById('budget-chart');
    if (!budgetChartEl) return;
    
    // Check if we have data from the template
    if (!window.chartData || !window.chartData.budget) return;
    
    const data = window.chartData.budget;
    
    new Chart(budgetChartEl, {
        type: 'bar',
        data: {
            labels: data.labels,
            datasets: [
                {
                    label: 'Budget',
                    data: data.budget,
                    backgroundColor: 'rgba(13, 110, 253, 0.5)',
                    borderColor: 'rgba(13, 110, 253, 1)',
                    borderWidth: 1
                },
                {
                    label: 'Spent',
                    data: data.spent,
                    backgroundColor: 'rgba(220, 53, 69, 0.5)',
                    borderColor: 'rgba(220, 53, 69, 1)',
                    borderWidth: 1
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

// Initialize income vs expense chart
function initializeIncomeExpenseChart() {
    const incomeExpenseChartEl = document.getElementById('income-expense-chart');
    if (!incomeExpenseChartEl) return;
    
    // Check if we have data from the template
    if (!window.chartData || !window.chartData.incomeExpense) return;
    
    const data = window.chartData.incomeExpense;
    
    new Chart(incomeExpenseChartEl, {
        type: 'bar',
        data: {
            labels: data.labels,
            datasets: [
                {
                    label: 'Income',
                    data: data.income,
                    backgroundColor: 'rgba(25, 135, 84, 0.5)',
                    borderColor: 'rgba(25, 135, 84, 1)',
                    borderWidth: 1
                },
                {
                    label: 'Expenses',
                    data: data.expenses,
                    backgroundColor: 'rgba(220, 53, 69, 0.5)',
                    borderColor: 'rgba(220, 53, 69, 1)',
                    borderWidth: 1
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

// Initialize spending trend chart
function initializeTrendChart() {
    const trendChartEl = document.getElementById('trend-chart');
    if (!trendChartEl) return;
    
    // Check if we have data from the template
    if (!window.chartData || !window.chartData.trend) return;
    
    const data = window.chartData.trend;
    
    new Chart(trendChartEl, {
        type: 'line',
        data: {
            labels: data.labels,
            datasets: [
                {
                    label: 'Income',
                    data: data.income,
                    fill: false,
                    backgroundColor: 'rgba(25, 135, 84, 1)',
                    borderColor: 'rgba(25, 135, 84, 1)',
                    tension: 0.1
                },
                {
                    label: 'Expenses',
                    data: data.expenses,
                    fill: false,
                    backgroundColor: 'rgba(220, 53, 69, 1)',
                    borderColor: 'rgba(220, 53, 69, 1)',
                    tension: 0.1
                },
                {
                    label: 'Balance',
                    data: data.balance,
                    fill: false,
                    backgroundColor: 'rgba(13, 110, 253, 1)',
                    borderColor: 'rgba(13, 110, 253, 1)',
                    tension: 0.1
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

// Function to load chart data from the API
function loadChartData(endpoint, params, callback) {
    const url = new URL(endpoint, window.location.origin);
    
    // Add params to URL
    if (params) {
        Object.keys(params).forEach(key => {
            url.searchParams.append(key, params[key]);
        });
    }
    
    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (callback && typeof callback === 'function') {
                callback(data);
            }
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
}

// Function to format currency values
function formatCurrency(value, currency = 'USD') {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: currency
    }).format(value);
}

// Function to format date values
function formatDate(dateString, format = 'medium') {
    const date = new Date(dateString);
    return new Intl.DateTimeFormat('en-US', {
        dateStyle: format
    }).format(date);
}

// Toggle advanced filters in forms
function toggleAdvancedFilters(button) {
    const filterSection = document.querySelector('.advanced-filters');
    if (!filterSection) return;
    
    filterSection.classList.toggle('d-none');
    
    if (filterSection.classList.contains('d-none')) {
        button.textContent = 'Show Advanced Filters';
    } else {
        button.textContent = 'Hide Advanced Filters';
    }
}