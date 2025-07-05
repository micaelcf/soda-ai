import { createContext, useContext, useState } from "react";
import type { ReactNode } from "react";
import config from "./config";

interface CustomerContextType {
  customerId: number;
  setCustomerId: (id: number) => void;
}

const CustomerContext = createContext<CustomerContextType | undefined>(
  undefined
);

export function CustomerProvider({ children }: { children: ReactNode }) {
  const [customerId, setCustomerId] = useState(config.defaultCustomerId);

  return (
    <CustomerContext.Provider value={{ customerId, setCustomerId }}>
      {children}
    </CustomerContext.Provider>
  );
}

export function useCustomer() {
  const context = useContext(CustomerContext);
  if (context === undefined) {
    throw new Error("useCustomer must be used within a CustomerProvider");
  }
  return context;
}
