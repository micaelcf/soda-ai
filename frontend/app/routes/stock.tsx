import { useState, useEffect } from "react";
import api from "../lib/api";
import { getStockStatus } from "../lib/utils";
import type { Soda } from "../lib/types";

export default function StockPage() {
  const [sodas, setSodas] = useState<Soda[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchStock();
  }, []);

  const fetchStock = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await api.getSodas();
      setSodas(data);
    } catch (err) {
      console.error("Error fetching stock:", err);
      setError(
        "Failed to load stock data. Please check if the backend server is running."
      );
      // Mock data for development/testing
      setSodas([
        { id: 1, name: "Coca-Cola", quantity: 15, price: 1.5 },
        { id: 2, name: "Pepsi", quantity: 12, price: 1.5 },
        { id: 3, name: "Sprite", quantity: 8, price: 1.45 },
        { id: 4, name: "Fanta", quantity: 10, price: 1.45 },
        { id: 5, name: "Dr Pepper", quantity: 6, price: 1.55 },
      ]);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="max-w-6xl mx-auto">
        <div className="flex items-center justify-center h-64">
          <div className="text-center">
            <div className="w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
            <p className="text-gray-400">Loading stock data...</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto">
      <div className="flex justify-between items-center mb-6">
        <div>
          <h2 className="text-3xl font-bold text-gray-50 mb-2">Soda Stock</h2>
          <p className="text-gray-400">
            Current inventory levels for all available sodas
          </p>
        </div>
        <button
          onClick={fetchStock}
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

      <div className="bg-gray-800 rounded-lg border border-gray-700 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-700">
              <tr>
                <th className="px-6 py-4 text-left text-sm font-medium text-gray-300 uppercase tracking-wider">
                  Soda Name
                </th>
                <th className="px-6 py-4 text-left text-sm font-medium text-gray-300 uppercase tracking-wider">
                  Quantity
                </th>
                <th className="px-6 py-4 text-left text-sm font-medium text-gray-300 uppercase tracking-wider">
                  Price
                </th>
                <th className="px-6 py-4 text-left text-sm font-medium text-gray-300 uppercase tracking-wider">
                  Status
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-700">
              {sodas.map((soda) => {
                const sodaStatus = getStockStatus(soda.quantity);
                return (
                  <tr
                    key={soda.id || soda.name}
                    className="hover:bg-gray-700/50 transition-colors"
                  >
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        <span className="text-2xl mr-3">🥤</span>
                        <div>
                          <div className="text-sm font-medium text-gray-50">
                            {soda.name}
                          </div>
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-50">
                        {soda.quantity} units
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-50">
                        ${soda.price.toFixed(2)}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span
                        className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${sodaStatus.color}`}
                      >
                        {sodaStatus.status}
                      </span>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>

        {sodas.length === 0 && !loading && (
          <div className="text-center py-12">
            <div className="text-gray-400 text-lg mb-2">🥤</div>
            <p className="text-gray-400">No sodas available in stock</p>
          </div>
        )}
      </div>
    </div>
  );
}
