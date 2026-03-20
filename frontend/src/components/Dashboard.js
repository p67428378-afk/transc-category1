import React, { useState, useEffect } from 'react';
import { Pie, Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
} from 'chart.js';

ChartJS.register(
  ArcElement,
  Tooltip,
  Legend,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title
);

function Dashboard({ transactions, categories, onFilterChange }) {
  const [selectedCategory, setSelectedCategory] = useState('');
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');

  useEffect(() => {
    const filters = {};
    if (selectedCategory) filters.category = selectedCategory;
    if (startDate) filters.start_date = startDate;
    if (endDate) filters.end_date = endDate;
    onFilterChange(filters);
  }, [selectedCategory, startDate, endDate]);

  // Aggregate data for Pie Chart (Spending by Category)
  const spendingByCategory = transactions.reduce((acc, transaction) => {
    const category = transaction.category || 'Uncategorized';
    acc[category] = (acc[category] || 0) + transaction.amount;
    return acc;
  }, {});

  const pieChartData = {
    labels: Object.keys(spendingByCategory),
    datasets: [
      {
        data: Object.values(spendingByCategory),
        backgroundColor: [
          '#FF6384',
          '#36A2EB',
          '#FFCE56',
          '#4BC0C0',
          '#9966CC',
          '#FF9F40',
          '#E7E9ED',
        ],
        hoverBackgroundColor: [
          '#FF6384',
          '#36A2EB',
          '#FFCE56',
          '#4BC0C0',
          '#9966CC',
          '#FF9F40',
          '#E7E9ED',
        ],
      },
    ],
  };

  // Aggregate data for Line Chart (Monthly Trends)
  const spendingByMonth = transactions.reduce((acc, transaction) => {
    const month = transaction.date ? transaction.date.substring(0, 7) : 'Unknown'; // YYYY-MM
    acc[month] = (acc[month] || 0) + transaction.amount;
    return acc;
  }, {});

  const sortedMonths = Object.keys(spendingByMonth).sort();
  const monthlySpendingData = sortedMonths.map(month => spendingByMonth[month]);

  const lineChartData = {
    labels: sortedMonths,
    datasets: [
      {
        label: 'Monthly Spending',
        data: monthlySpendingData,
        fill: false,
        borderColor: 'rgb(75, 192, 192)',
        tension: 0.1,
      },
    ],
  };

  return (
    <div>
      <div className="dashboard-filters">
        <label>
          Category:
          <select onChange={(e) => setSelectedCategory(e.target.value)} value={selectedCategory}>
            <option value="">All</option>
            {categories.map((cat) => (
              <option key={cat} value={cat}>
                {cat}
              </option>
            ))}
          </select>
        </label>
        <label>
          Start Date:
          <input type="date" onChange={(e) => setStartDate(e.target.value)} value={startDate} />
        </label>
        <label>
          End Date:
          <input type="date" onChange={(e) => setEndDate(e.target.value)} value={endDate} />
        </label>
      </div>

      <div className="dashboard-charts">
        <div className="chart-container">
          <h3>Spending by Category</h3>
          {transactions.length > 0 ? <Pie data={pieChartData} /> : <p>No data to display for spending by category.</p>}
        </div>
        <div className="chart-container">
          <h3>Monthly Spending Trends</h3>
          {transactions.length > 0 ? <Line data={lineChartData} /> : <p>No data to display for monthly trends.</p>}
        </div>
      </div>

      <h3>All Transactions</h3>
      {transactions.length > 0 ? (
        <table className="transactions-table">
          <thead>
            <tr>
              <th>Date</th>
              <th>Merchant</th>
              <th>Amount</th>
              <th>Category</th>
              <th>Description</th>
            </tr>
          </thead>
          <tbody>
            {transactions.map((transaction, index) => (
              <tr key={index}>
                <td>{transaction.date}</td>
                <td>{transaction.merchant}</td>
                <td>{transaction.amount.toFixed(2)}</td>
                <td>{transaction.category || 'Uncategorized'}</td>
                <td>{transaction.description}</td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <p>No transactions to display.</p>
      )}
    </div>
  );
}

export default Dashboard;
