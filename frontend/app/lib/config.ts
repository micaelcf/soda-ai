// Environment configuration
export const config = {
  apiUrl:
    process.env.NODE_ENV === "production"
      ? "http://localhost:8000" // Update this for production
      : "http://localhost:8000",

  // API endpoints - Updated to match your backend
  endpoints: {
    userQuery: "/query/actions",
    sodas: "/soda",
    transactionsByCustomer: "/transaction/customer",
  },

  // App settings
  app: {
    name: "Soda AI",
    description: "AI-Powered Vending Machine",
    version: "1.0.0",
  },

  // Chat settings
  chat: {
    maxMessageLength: 500,
    typingDelay: 100,
    maxRetries: 3,
  },

  // Default customer ID (changeable in UI)
  defaultCustomerId: 1,
};

export default config;
