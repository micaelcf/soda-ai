import { useState, useRef, useEffect } from "react";
import api from "../lib/api";
import { useCustomer } from "../lib/customer-context";
import type { Message } from "../lib/types";

export function IcBaselineSend(props: React.SVGProps<SVGSVGElement>) {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width="1em"
      height="1em"
      viewBox="0 0 24 24"
      {...props}
    >
      <path
        fill="currentColor"
        d="M2.01 21L23 12L2.01 3L2 10l15 2l-15 2z"
      ></path>
    </svg>
  );
}

export function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "1",
      content:
        "Hello! I'm your Soda AI assistant. I can help you buy sodas, check stock, and view your purchase history. <br><br> I can handle many tasks with one single message! <br><br>What would you like to do today?",
      sender: "ai",
      timestamp: new Date(),
    },
  ]);
  const [inputValue, setInputValue] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const { customerId } = useCustomer();

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const formatActionsResponse = (
    actionsExecuted: Awaited<ReturnType<typeof api.sendUserQuery>>
  ): string => {
    if (!actionsExecuted.data || actionsExecuted.data.length === 0) {
      return "I processed your request, but I'm not sure what to respond with.";
    }
    const messageHeading = (msg: string) => `<br>✅ ${msg} <br><br>`;

    return actionsExecuted.data
      .map(({ data, error }, i) => {
        if (error || !data) {
          return `<br><br>Sorry, there was an error: ${error?.message}<br><br>`;
        }
        if (typeof data === "string") {
          return messageHeading("General Response:") + data;
        }
        if (Array.isArray(data)) {
          return (
            messageHeading("Checking transaction history:") +
            "I processed your request. Here your transaction history:<br>" +
            data.map((item) => JSON.stringify(item)).join("<br>")
          );
        }
        if ("timestamp" in data && "quantity" in data) {
          return (
            messageHeading("Purchasing a soda:") +
            `Great! I'll help you purchase ${data.quantity} of soda_id: ${data.soda_id}(s).<br>`
          );
        }
        return (
          messageHeading("Inventory management:") +
          "The soda that you managed is: <br>" +
          JSON.stringify(data, null, 2) +
          "<br>"
        );
      })
      .join(" ");
  };

  const sendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      content: inputValue,
      sender: "user",
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputValue("");
    setIsLoading(true);

    try {
      const response = await api.sendUserQuery(customerId, inputValue);

      let aiContent = "I processed your request.";

      if (response.data) {
        aiContent = formatActionsResponse(response);
      } else if (response.error) {
        aiContent = `Sorry, there was an error: ${response.error.message}`;
      }

      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: aiContent,
        sender: "ai",
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, aiMessage]);
    } catch (error) {
      console.error("Error sending message:", error);
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        content:
          "Sorry, I'm having trouble connecting to the server right now. Please try again later.",
        sender: "ai",
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="flex flex-col h-[512px]">
      {/* Messages */}
      <div className="flex-1 overflow-y-auto space-y-4 mb-4 p-4 bg-gray-900 rounded-lg border border-gray-600">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex ${
              message.sender === "user" ? "justify-end" : "justify-start"
            }`}
          >
            <div
              className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                message.sender === "user"
                  ? "bg-blue-600 text-white"
                  : "bg-gray-700 text-gray-50"
              }`}
            >
              <p
                className="text-sm max-w-full"
                dangerouslySetInnerHTML={{
                  __html: message.content.startsWith("<br>")
                    ? message.content.slice(4) // Remove leading <br> if present
                    : message.content,
                }}
              />
              <p
                className={`text-xs mt-1 ${
                  message.sender === "user" ? "text-blue-100" : "text-gray-400"
                }`}
              >
                {message.timestamp.toLocaleTimeString()}
              </p>
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-gray-700 text-gray-50 max-w-xs lg:max-w-md px-4 py-2 rounded-lg">
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                <div
                  className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"
                  style={{ animationDelay: "0.1s" }}
                ></div>
                <div
                  className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"
                  style={{ animationDelay: "0.2s" }}
                ></div>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="flex space-x-2">
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Type your message here..."
          className="flex-1 px-4 py-2 bg-gray-700 border border-gray-600 rounded-lg text-gray-50 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          disabled={isLoading}
        />
        <button
          onClick={sendMessage}
          disabled={isLoading || !inputValue.trim()}
          className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 focus:outline-none  flex items-center gap-3
          focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 focus:ring-offset-gray-800 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          <IcBaselineSend className="w-5 h-5" />
          Send
        </button>
      </div>
    </div>
  );
}
