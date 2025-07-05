# 🤖 Soda AI Frontend

A modern, responsive React frontend for the Soda AI vending machine API built with React Router and Tailwind CSS.

## ✨ Features

- **Dark Theme Interface** with gray-50 text color
- **Responsive Design** that works on desktop and mobile
- **Clean Component Architecture** following React best practices
- **Real-time Chat Interface** for natural language interaction
- **Stock Management** view with live inventory data
- **Transaction History** with detailed purchase records
- **Rounded borders** and clean, spaced table structures

## 🏗️ Architecture

### Pages

- **Chat Page** (`/`) - Interactive chat interface for natural language soda purchasing
- **Stock Page** (`/stock`) - Real-time view of soda inventory with stock levels
- **History Page** (`/history`) - Complete transaction history with summaries

### Components

- **MainLayout** - Primary layout with sidebar navigation and responsive mobile menu
- **ChatInterface** - Real-time chat component with message history
- **API Integration** - Centralized API client for backend communication

## 🚀 Getting Started

### Prerequisites

- Node.js 18+ installed
- Your Soda AI backend running on `http://localhost:8000`

### Installation

1. Navigate to the frontend directory:

```bash
cd frontend
```

2. Install dependencies:

```bash
npm install
```

3. Start the development server:

```bash
npm run dev
```

4. Open your browser to `http://localhost:5173`

### Building for Production

```bash
npm run build
npm run start
```

## 🔧 Configuration

### Backend API URL

Update the API base URL in `app/lib/api.ts`:

```typescript
const API_BASE_URL = "http://localhost:8000"; // Change to your backend URL
```

### Styling

The app uses Tailwind CSS with a dark theme. Main styles are in `app/app.css`.

## 📱 Mobile Support

The interface is fully responsive with:

- Collapsible sidebar navigation on mobile
- Touch-friendly interaction elements
- Optimized layouts for small screens

## 🎨 Design System

- **Primary Colors**: Blue (600/700) for interactive elements
- **Background**: Gray (900/800) for dark theme
- **Text**: Gray (50) for primary text, Gray (400) for secondary
- **Borders**: Gray (700) for subtle divisions
- **Success**: Green for positive states
- **Warning**: Yellow for alerts
- **Error**: Red for error states

## 🔗 API Integration

The frontend is now fully integrated with your backend OpenAPI specification. Here are the endpoints used:

### **Backend Endpoints**

- **`POST /query/actions`** - Used in the Chat page for natural language processing
  - Sends user queries with customer ID
  - Receives structured actions based on user intent
- **`GET /soda`** - Used in the Stock page for inventory display
  - Fetches all available sodas with quantities and prices
  - Updates stock status indicators
- **`GET /transaction/customer/{customer_id}`** - Used in the History page
  - Fetches transaction history for specific customer
  - Enhanced with soda details for better display

### **Customer ID Management**

- Global customer context with default ID = 1
- Customer ID selector in the header (desktop and mobile)
- All API calls use the selected customer ID
- Customer ID is displayed on relevant pages

### **Data Enhancement**

- Transaction data is enhanced with soda names and calculated totals
- Stock status indicators with color coding
- Proper error handling with fallback to mock data
- Loading states and refresh functionality

### **API Configuration**

Update the API base URL in `app/lib/config.ts` if your backend runs on a different port:

```typescript
export const config = {
  apiUrl: "http://localhost:8000", // Change this to your backend URL
  // ...
};
```

### **CORS Configuration**

Make sure your FastAPI backend has CORS enabled for the frontend domain:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],  # Add your frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 📦 Technologies Used

- **React 19** - UI framework
- **React Router 7** - Routing and navigation
- **Tailwind CSS 4** - Styling and design system
- **TypeScript** - Type safety
- **Vite** - Build tool and dev server

## 🤝 Contributing

1. Follow the established component patterns
2. Use TypeScript for all new files
3. Maintain the dark theme consistency
4. Ensure responsive design for all new components
5. Add proper error handling for API calls
