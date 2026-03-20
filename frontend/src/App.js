import React, { useState, useEffect } from 'react';
import UploadForm from './components/UploadForm';
import Dashboard from './components/Dashboard';
import './App.css';

function App() {
  const [categories, setCategories] = useState([]);
  const [transactions, setTransactions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:5000/api';

  const fetchCategories = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/categories`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      setCategories(data);
    } catch (e) {
      console.error("Error fetching categories:", e);
      setError("Failed to load categories.");
    }
  };

  const fetchTransactions = async (filters = {}) => {
    setLoading(true);
    setError(null);
    try {
      const params = new URLSearchParams(filters);
      const response = await fetch(`${API_BASE_URL}/reports?${params.toString()}`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      setTransactions(data);
    } catch (e) {
      console.error("Error fetching transactions:", e);
      setError("Failed to load transactions.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCategories();
    fetchTransactions();
  }, []);

  const handleUploadSuccess = () => {
    fetchTransactions(); // Refresh transactions after upload
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Transaction Categorization Dashboard</h1>
      </header>
      <main>
        <section className="upload-section">
          <h2>Upload Transactions</h2>
          <UploadForm onUploadSuccess={handleUploadSuccess} apiBaseUrl={API_BASE_URL} />
        </section>
        <section className="dashboard-section">
          <h2>Spending Dashboard</h2>
          {loading && <p>Loading transactions...</p>}
          {error && <p className="error-message">{error}</p>}
          {!loading && !error && (
            <Dashboard
              transactions={transactions}
              categories={categories}
              onFilterChange={fetchTransactions}
            />
          )}
        </section>
      </main>
    </div>
  );
}

export default App;
