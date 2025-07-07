import { Outlet, Link, useLocation } from "react-router";
import { useState } from "react";
import { useCustomer } from "../lib/customer-context";

export default function MainLayout() {
  const location = useLocation();
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const { customerId, setCustomerId } = useCustomer();

  const navigation = [
    { name: "Chat", href: "/", icon: "💬" },
    { name: "Soda Stock", href: "/stock", icon: "🥤" },
    { name: "History", href: "/history", icon: "📋" },
  ];

  return (
    <div className="min-h-dvh bg-gray-900 text-gray-50">
      {/* Header */}
      <header className="bg-gray-800 border-b px-6 py-4 border-gray-700 flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
            🤖 Soda AI
          </h1>
          <p className="text-gray-400 text-sm mt-1">
            AI-Powered Vending Machine
          </p>
        </div>
        <div className="flex items-center space-x-4">
          {/* Customer ID Selector */}
          <div className="hidden md:flex items-center space-x-2">
            <label htmlFor="customer-id" className="text-sm text-gray-400">
              Customer ID:
            </label>
            <input
              id="customer-id"
              type="number"
              min="1"
              value={customerId}
              onChange={(e) => setCustomerId(parseInt(e.target.value) || 1)}
              className="w-20 px-2 py-1 bg-gray-700 border border-gray-600 rounded text-gray-50 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          {/* Mobile menu button */}
          <button
            onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
            className="md:hidden p-2 rounded-lg text-gray-400 hover:text-gray-50 hover:bg-gray-700 transition-colors"
          >
            <svg
              className="w-6 h-6"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d={
                  isMobileMenuOpen
                    ? "M6 18L18 6M6 6l12 12"
                    : "M4 6h16M4 12h16M4 18h16"
                }
              />
            </svg>
          </button>
        </div>
      </header>

      <div className="flex">
        {/* Sidebar - Desktop */}
        <nav className="hidden md:block w-64 bg-gray-800 border-r border-gray-700 min-h-[calc(100dvh-89px)]">
          <div className="p-4">
            <ul className="space-y-2">
              {navigation.map((item) => (
                <li key={item.name}>
                  <Link
                    to={item.href}
                    className={`flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors ${
                      location.pathname === item.href
                        ? "bg-blue-600 text-white"
                        : "text-gray-300 hover:bg-gray-700 hover:text-white"
                    }`}
                  >
                    <span className="text-lg">{item.icon}</span>
                    <span className="font-medium">{item.name}</span>
                  </Link>
                </li>
              ))}
            </ul>
          </div>
        </nav>

        {/* Mobile Menu */}
        {isMobileMenuOpen && (
          <div className="fixed inset-0 z-50 md:hidden">
            <div
              className="fixed inset-0 bg-gray-900/50"
              onClick={() => setIsMobileMenuOpen(false)}
            />
            <nav className="fixed top-0 left-0 bottom-0 w-64 bg-gray-800 border-r border-gray-700">
              <div className="p-4">
                <div className="flex items-center justify-between mb-6">
                  <h2 className="text-lg font-semibold text-gray-50">Menu</h2>
                  <button
                    onClick={() => setIsMobileMenuOpen(false)}
                    className="p-2 rounded-lg text-gray-400 hover:text-gray-50 hover:bg-gray-700"
                  >
                    <svg
                      className="w-5 h-5"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M6 18L18 6M6 6l12 12"
                      />
                    </svg>
                  </button>
                </div>

                {/* Mobile Customer ID Selector */}
                <div className="flex items-center space-x-2 mb-6 p-3 bg-gray-700 rounded-lg">
                  <label
                    htmlFor="mobile-customer-id"
                    className="text-sm text-gray-400"
                  >
                    Customer ID:
                  </label>
                  <input
                    id="mobile-customer-id"
                    type="number"
                    min="1"
                    value={customerId}
                    onChange={(e) =>
                      setCustomerId(parseInt(e.target.value) || 1)
                    }
                    className="flex-1 px-2 py-1 w-12 bg-gray-600 border border-gray-500 rounded text-gray-50 text-sm 
                    focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
                <ul className="space-y-2">
                  {navigation.map((item) => (
                    <li key={item.name}>
                      <Link
                        to={item.href}
                        onClick={() => setIsMobileMenuOpen(false)}
                        className={`flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors ${
                          location.pathname === item.href
                            ? "bg-blue-600 text-white"
                            : "text-gray-300 hover:bg-gray-700 hover:text-white"
                        }`}
                      >
                        <span className="text-lg">{item.icon}</span>
                        <span className="font-medium">{item.name}</span>
                      </Link>
                    </li>
                  ))}
                </ul>
              </div>
            </nav>
          </div>
        )}

        {/* Main Content */}
        <main className="flex-1 p-4 md:p-6">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
