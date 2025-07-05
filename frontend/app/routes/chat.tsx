import { useState } from "react";
import { ChatInterface } from "../components/ChatInterface";
import { useCustomer } from "../lib/customer-context";

export default function ChatPage() {
  const { customerId } = useCustomer();

  return (
    <div className="max-w-4xl mx-auto">
      <div className="mb-6">
        <h2 className="text-3xl font-bold text-gray-50 mb-2">
          Chat with Soda AI
        </h2>
        <p className="text-gray-400">
          Chatting as Customer ID:{" "}
          <span className="text-blue-400 font-medium">{customerId}</span> - Ask
          me anything about buying sodas, checking stock, or your purchase
          history!
        </p>
      </div>

      <div className="bg-gray-800 rounded-lg border border-gray-700 p-6">
        <ChatInterface />
      </div>
    </div>
  );
}
