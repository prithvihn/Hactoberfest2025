import React, { useState, useMemo } from 'react';
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import { Wallet, TrendingUp, TrendingDown, DollarSign, Plus, Trash2, Calendar, Tag } from 'lucide-react';

const categories = [
  { name: 'Food', color: '#FF6B6B', icon: '🍕' },
  { name: 'Transport', color: '#4ECDC4', icon: '🚗' },
  { name: 'Entertainment', color: '#FFE66D', icon: '🎮' },
  { name: 'Shopping', color: '#95E1D3', icon: '🛍️' },
  { name: 'Bills', color: '#C7CEEA', icon: '💳' },
  { name: 'Health', color: '#FFDAB9', icon: '⚕️' },
  { name: 'Education', color: '#B4A7D6', icon: '📚' },
  { name: 'Others', color: '#A8DADC', icon: '📦' }
];

export default function ExpenseTracker() {
  const [expenses, setExpenses] = useState([
    { id: 1, name: 'Lunch at Restaurant', amount: 25.50, category: 'Food', date: '2025-10-20' },
    { id: 2, name: 'Uber Ride', amount: 15.00, category: 'Transport', date: '2025-10-20' },
    { id: 3, name: 'Movie Tickets', amount: 30.00, category: 'Entertainment', date: '2025-10-19' },
    { id: 4, name: 'Grocery Shopping', amount: 85.75, category: 'Food', date: '2025-10-18' }
  ]);

  const [formData, setFormData] = useState({
    name: '',
    amount: '',
    category: 'Food',
    date: new Date().toISOString().split('T')[0]
  });

  const [filter, setFilter] = useState('all');
  const [sortBy, setSortBy] = useState('date');

  // Calculate statistics
  const stats = useMemo(() => {
    const total = expenses.reduce((sum, exp) => sum + exp.amount, 0);
    const thisMonth = expenses.filter(exp => {
      const expDate = new Date(exp.date);
      const now = new Date();
      return expDate.getMonth() === now.getMonth() && 
             expDate.getFullYear() === now.getFullYear();
    }).reduce((sum, exp) => sum + exp.amount, 0);

    const categoryData = categories.map(cat => ({
      name: cat.name,
      value: expenses
        .filter(exp => exp.category === cat.name)
        .reduce((sum, exp) => sum + exp.amount, 0),
      color: cat.color
    })).filter(item => item.value > 0);

    const last7Days = Array.from({ length: 7 }, (_, i) => {
      const date = new Date();
      date.setDate(date.getDate() - (6 - i));
      const dateStr = date.toISOString().split('T')[0];
      const dayExpenses = expenses
        .filter(exp => exp.date === dateStr)
        .reduce((sum, exp) => sum + exp.amount, 0);
      
      return {
        date: date.toLocaleDateString('en-US', { weekday: 'short' }),
        amount: dayExpenses
      };
    });

    return { total, thisMonth, categoryData, last7Days };
  }, [expenses]);

  const handleAddExpense = (e) => {
    e.preventDefault();
    if (formData.name && formData.amount) {
      const newExpense = {
        id: Date.now(),
        name: formData.name,
        amount: parseFloat(formData.amount),
        category: formData.category,
        date: formData.date
      };
      setExpenses([newExpense, ...expenses]);
      setFormData({
        name: '',
        amount: '',
        category: 'Food',
        date: new Date().toISOString().split('T')[0]
      });
    }
  };

  const handleDeleteExpense = (id) => {
    setExpenses(expenses.filter(exp => exp.id !== id));
  };

  const filteredExpenses = useMemo(() => {
    let filtered = expenses;
    
    if (filter !== 'all') {
      filtered = filtered.filter(exp => exp.category === filter);
    }

    return filtered.sort((a, b) => {
      if (sortBy === 'date') return new Date(b.date) - new Date(a.date);
      if (sortBy === 'amount') return b.amount - a.amount;
      return a.name.localeCompare(b.name);
    });
  }, [expenses, filter, sortBy]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-pink-50 to-blue-50 p-4 md:p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="flex items-center justify-center gap-3 mb-2">
            <Wallet className="w-10 h-10 text-purple-600" />
            <h1 className="text-4xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
              Smart Expense Tracker
            </h1>
          </div>
          <p className="text-gray-600">Take control of your finances with intelligent tracking</p>
        </div>

        {/* Statistics Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white rounded-2xl shadow-lg p-6 border-l-4 border-purple-500">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-500 text-sm font-medium">Total Expenses</p>
                <p className="text-3xl font-bold text-gray-800 mt-1">${stats.total.toFixed(2)}</p>
              </div>
              <div className="bg-purple-100 p-3 rounded-full">
                <DollarSign className="w-8 h-8 text-purple-600" />
              </div>
            </div>
          </div>

          <div className="bg-white rounded-2xl shadow-lg p-6 border-l-4 border-pink-500">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-500 text-sm font-medium">This Month</p>
                <p className="text-3xl font-bold text-gray-800 mt-1">${stats.thisMonth.toFixed(2)}</p>
              </div>
              <div className="bg-pink-100 p-3 rounded-full">
                <TrendingUp className="w-8 h-8 text-pink-600" />
              </div>
            </div>
          </div>

          <div className="bg-white rounded-2xl shadow-lg p-6 border-l-4 border-blue-500">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-500 text-sm font-medium">Total Transactions</p>
                <p className="text-3xl font-bold text-gray-800 mt-1">{expenses.length}</p>
              </div>
              <div className="bg-blue-100 p-3 rounded-full">
                <Tag className="w-8 h-8 text-blue-600" />
              </div>
            </div>
          </div>
        </div>

        {/* Main Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left Column - Add Expense Form */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-2xl shadow-lg p-6">
              <h2 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
                <Plus className="w-5 h-5" />
                Add New Expense
              </h2>
              
              <form onSubmit={handleAddExpense} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
                  <input
                    type="text"
                    value={formData.name}
                    onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                    placeholder="e.g., Coffee at Starbucks"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Amount ($)</label>
                  <input
                    type="number"
                    step="0.01"
                    value={formData.amount}
                    onChange={(e) => setFormData({ ...formData, amount: e.target.value })}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                    placeholder="0.00"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Category</label>
                  <select
                    value={formData.category}
                    onChange={(e) => setFormData({ ...formData, category: e.target.value })}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                  >
                    {categories.map(cat => (
                      <option key={cat.name} value={cat.name}>
                        {cat.icon} {cat.name}
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Date</label>
                  <input
                    type="date"
                    value={formData.date}
                    onChange={(e) => setFormData({ ...formData, date: e.target.value })}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                    required
                  />
                </div>

                <button
                  type="submit"
                  className="w-full bg-gradient-to-r from-purple-600 to-pink-600 text-white py-3 rounded-lg font-semibold hover:shadow-lg transition-all duration-200 transform hover:scale-105"
                >
                  Add Expense
                </button>
              </form>
            </div>

            {/* Category Distribution */}
            {stats.categoryData.length > 0 && (
              <div className="bg-white rounded-2xl shadow-lg p-6 mt-6">
                <h3 className="text-lg font-bold text-gray-800 mb-4">Category Distribution</h3>
                <ResponsiveContainer width="100%" height={250}>
                  <PieChart>
                    <Pie
                      data={stats.categoryData}
                      dataKey="value"
                      nameKey="name"
                      cx="50%"
                      cy="50%"
                      outerRadius={80}
                      label={(entry) => `${entry.name}: $${entry.value.toFixed(0)}`}
                    >
                      {stats.categoryData.map((entry, index) => (
                        <Cell key={index} fill={entry.color} />
                      ))}
                    </Pie>
                    <Tooltip formatter={(value) => `$${value.toFixed(2)}`} />
                  </PieChart>
                </ResponsiveContainer>
              </div>
            )}
          </div>

          {/* Right Column - Expenses List & Charts */}
          <div className="lg:col-span-2 space-y-6">
            {/* Weekly Spending Chart */}
            <div className="bg-white rounded-2xl shadow-lg p-6">
              <h3 className="text-lg font-bold text-gray-800 mb-4">Last 7 Days Spending</h3>
              <ResponsiveContainer width="100%" height={200}>
                <BarChart data={stats.last7Days}>
                  <XAxis dataKey="date" />
                  <YAxis />
                  <Tooltip formatter={(value) => `$${value.toFixed(2)}`} />
                  <Bar dataKey="amount" fill="#8b5cf6" radius={[8, 8, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>

            {/* Filters */}
            <div className="bg-white rounded-2xl shadow-lg p-6">
              <div className="flex flex-col sm:flex-row gap-4 mb-4">
                <div className="flex-1">
                  <label className="block text-sm font-medium text-gray-700 mb-2">Filter by Category</label>
                  <select
                    value={filter}
                    onChange={(e) => setFilter(e.target.value)}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500"
                  >
                    <option value="all">All Categories</option>
                    {categories.map(cat => (
                      <option key={cat.name} value={cat.name}>{cat.icon} {cat.name}</option>
                    ))}
                  </select>
                </div>

                <div className="flex-1">
                  <label className="block text-sm font-medium text-gray-700 mb-2">Sort By</label>
                  <select
                    value={sortBy}
                    onChange={(e) => setSortBy(e.target.value)}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500"
                  >
                    <option value="date">Date (Newest)</option>
                    <option value="amount">Amount (Highest)</option>
                    <option value="name">Name (A-Z)</option>
                  </select>
                </div>
              </div>

              {/* Expenses List */}
              <div className="space-y-3 max-h-96 overflow-y-auto">
                {filteredExpenses.length === 0 ? (
                  <div className="text-center py-8 text-gray-500">
                    <p>No expenses found. Add your first expense!</p>
                  </div>
                ) : (
                  filteredExpenses.map(expense => {
                    const category = categories.find(cat => cat.name === expense.category);
                    return (
                      <div
                        key={expense.id}
                        className="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:shadow-md transition-shadow"
                      >
                        <div className="flex items-center gap-4 flex-1">
                          <div
                            className="w-12 h-12 rounded-full flex items-center justify-center text-2xl"
                            style={{ backgroundColor: category.color + '30' }}
                          >
                            {category.icon}
                          </div>
                          <div className="flex-1">
                            <p className="font-semibold text-gray-800">{expense.name}</p>
                            <div className="flex items-center gap-3 mt-1 text-sm text-gray-500">
                              <span className="flex items-center gap-1">
                                <Tag className="w-3 h-3" />
                                {expense.category}
                              </span>
                              <span className="flex items-center gap-1">
                                <Calendar className="w-3 h-3" />
                                {new Date(expense.date).toLocaleDateString()}
                              </span>
                            </div>
                          </div>
                        </div>
                        <div className="flex items-center gap-4">
                          <p className="text-xl font-bold text-gray-800">
                            ${expense.amount.toFixed(2)}
                          </p>
                          <button
                            onClick={() => handleDeleteExpense(expense.id)}
                            className="p-2 text-red-500 hover:bg-red-50 rounded-lg transition-colors"
                          >
                            <Trash2 className="w-5 h-5" />
                          </button>
                        </div>
                      </div>
                    );
                  })
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
