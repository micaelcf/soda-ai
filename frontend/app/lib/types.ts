// Type definitions for the Soda AI frontend based on your OpenAPI spec

// Backend API Types
export interface Soda {
  id?: number | null;
  name: string;
  price: number;
  quantity: number;
}

export interface TransactionCustomer {
  id?: number | null;
  timestamp: string;
  quantity: number;
  soda_id?: number | null;
  customer_id?: number | null;
}

export interface UserQueryInput {
  customer_id: number;
  query: string;
}

export interface UserActions {
  actions: Array<
    | PurchaseAction
    | InventoryManagementAction
    | TransactionHistoryAction
    | GeneralAction
  >;
}

export interface PurchaseAction {
  intent: "purchase";
  soda_name: string;
  quantity: number;
}

export interface InventoryManagementAction {
  intent: "manage_inventory";
  operation: "add" | "read" | "remove" | "update";
  soda: Soda;
}

export interface TransactionHistoryAction {
  intent: "check_transactions_history";
  customer: {
    id?: number | null;
    name: string;
    email: string;
  };
}

export interface GeneralAction {
  intent: "greeting" | "unsupported";
  message: string;
}

export interface AppResponse<T = any> {
  data?: T | null;
  error?: {
    message: string;
    cause: string;
  } | null;
}

// Frontend UI Types
export interface Message {
  id: string;
  content: string;
  sender: "user" | "ai";
  timestamp: Date;
}

export interface NavigationItem {
  name: string;
  href: string;
  icon: string;
}

// Extended types for better UI representation
export interface EnhancedTransaction extends TransactionCustomer {
  soda_name?: string;
  total_price?: number;
}
