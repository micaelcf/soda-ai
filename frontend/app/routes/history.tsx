import { useState, useEffect } from "react";
import api from "../lib/api";
import { useCustomer } from "../lib/customer-context";
import { enhanceTransactionsWithSodaData, formatDateTime } from "../lib/utils";
import type {
  TransactionCustomer,
  EnhancedTransaction,
  Soda,
} from "../lib/types";

export default function HistoryPage() {
  const [transactions, setTransactions] = useState<EnhancedTransaction[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { customerId } = useCustomer();

  useEffect(() => {
    fetchHistory();
  }, [customerId]);

  const fetchHistory = async () => {
    try {
      setLoading(true);
      setError(null);

      // Fetch both transactions and sodas to enhance the display
      const [transactionData, sodaData] = await Promise.all([
        api.getTransactionsByCustomer(customerId),
        api.getSodas(),
      ]);

      // Enhance transactions with soda information
      const enhancedTransactions = await enhanceTransactionsWithSodaData(
        transactionData,
        sodaData
      );
      setTransactions(enhancedTransactions);
    } catch (err) {
      console.error("Error fetching history:", err);
      setError(
        "Failed to load transaction history. Please check if the backend server is running."
      );
      // Mock data for development/testing
      setTransactions([
        {
          id: 1,
          timestamp: new Date(Date.now() - 86400000).toISOString(),
          quantity: 2,
          soda_id: 1,
          customer_id: customerId,
          soda_name: "Coca-Cola",
          total_price: 3.0,
        },
        {
          id: 2,
          timestamp: new Date(Date.now() - 172800000).toISOString(),
          quantity: 1,
          soda_id: 2,
          customer_id: customerId,
          soda_name: "Pepsi",
          total_price: 1.5,
        },
        {
          id: 3,
          timestamp: new Date(Date.now() - 259200000).toISOString(),
          quantity: 3,
          soda_id: 3,
          customer_id: customerId,
          soda_name: "Sprite",
          total_price: 4.35,
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const refreshHistory = () => {
    fetchHistory();
  };

  const formatDate = (timestamp: string) => {
    return formatDateTime(timestamp);
  };

  const calculateTotal = () => {
    return transactions.reduce(
      (sum, transaction) => sum + (transaction.total_price || 0),
      0
    );
  };

  if (loading) {
    return (
      <div className="max-w-6xl mx-auto">
        <div className="flex items-center justify-center h-64">
          <div className="text-center">
            <div className="w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
            <p className="text-gray-400">Loading transaction history...</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto">
      <div className="flex justify-between items-center mb-6">
        <div>
          <h2 className="text-3xl font-bold text-gray-50 mb-2">
            Transaction History
          </h2>
          <p className="text-gray-400">
            Complete history for Customer ID:{" "}
            <span className="text-blue-400 font-medium">{customerId}</span>
          </p>
        </div>
        <button
          onClick={refreshHistory}
          className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 focus:ring-offset-gray-900 transition-colors"
        >
          🔄 Refresh
        </button>
      </div>

      {error && (
        <div className="bg-red-900 border border-red-700 text-red-300 px-4 py-3 rounded-lg mb-6">
          <p>{error}</p>
        </div>
      )}

      {/* Summary Card */}
      <div className="bg-gray-800 rounded-lg border border-gray-700 p-6 mb-6">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="text-center">
            <div className="text-2xl font-bold text-blue-400">
              {transactions.length}
            </div>
            <div className="text-sm text-gray-400">Total Transactions</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-green-400">
              {transactions.reduce((sum, t) => sum + t.quantity, 0)}
            </div>
            <div className="text-sm text-gray-400">Items Purchased</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-purple-400">
              ${calculateTotal().toFixed(2)}
            </div>
            <div className="text-sm text-gray-400">Total Spent</div>
          </div>
        </div>
      </div>

      <div className="bg-gray-800 rounded-lg border border-gray-700 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-700">
              <tr>
                <th className="px-6 py-4 text-left text-sm font-medium text-gray-300 uppercase tracking-wider">
                  Date & Time
                </th>
                <th className="px-6 py-4 text-left text-sm font-medium text-gray-300 uppercase tracking-wider">
                  Soda
                </th>
                <th className="px-6 py-4 text-left text-sm font-medium text-gray-300 uppercase tracking-wider">
                  Quantity
                </th>
                <th className="px-6 py-4 text-left text-sm font-medium text-gray-300 uppercase tracking-wider">
                  Total Price
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-700">
              {transactions.map((transaction) => (
                <tr
                  key={transaction.id || `tx-${transaction.timestamp}`}
                  className="hover:bg-gray-700/50 transition-colors"
                >
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm text-gray-50">
                      {formatDate(transaction.timestamp)}
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center">
                      <span className="text-xl mr-3">🥤</span>
                      <div className="text-sm font-medium text-gray-50">
                        {transaction.soda_name ||
                          `Soda ID ${transaction.soda_id}`}
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm text-gray-50">
                      {transaction.quantity}{" "}
                      {transaction.quantity === 1 ? "unit" : "units"}
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm font-medium text-green-400">
                      ${(transaction.total_price || 0).toFixed(2)}
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {transactions.length === 0 && !loading && (
          <div className="text-center py-12">
            <div className="text-gray-400 text-lg mb-2">📋</div>
            <p className="text-gray-400">No transactions found</p>
            <p className="text-gray-500 text-sm mt-2">
              Start by purchasing some sodas through the chat!
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
