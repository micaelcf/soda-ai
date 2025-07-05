// Utility functions for data transformation and formatting

import type { TransactionCustomer, Soda, EnhancedTransaction } from "./types";

/**
 * Enhance transaction data with soda information
 */
export async function enhanceTransactionsWithSodaData(
  transactions: TransactionCustomer[],
  sodas: Soda[]
): Promise<EnhancedTransaction[]> {
  return transactions.map((transaction) => {
    const soda = sodas.find((s) => s.id === transaction.soda_id);

    return {
      ...transaction,
      soda_name: soda?.name || `Unknown Soda (ID: ${transaction.soda_id})`,
      total_price: soda ? soda.price * transaction.quantity : 0,
    };
  });
}

/**
 * Format currency values
 */
export function formatCurrency(amount: number): string {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
  }).format(amount);
}

/**
 * Format date and time
 */
export function formatDateTime(timestamp: string): string {
  return new Date(timestamp).toLocaleString("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

/**
 * Get stock status based on quantity
 */
export function getStockStatus(quantity: number): {
  status: string;
  color: string;
} {
  if (quantity > 10) {
    return { status: "In Stock", color: "bg-green-900 text-green-300" };
  } else if (quantity > 5) {
    return { status: "Low Stock", color: "bg-yellow-900 text-yellow-300" };
  } else if (quantity > 0) {
    return { status: "Very Low", color: "bg-red-900 text-red-300" };
  } else {
    return { status: "Out of Stock", color: "bg-gray-700 text-gray-400" };
  }
}
