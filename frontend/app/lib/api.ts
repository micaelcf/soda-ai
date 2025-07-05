// API client updated to match your backend OpenAPI specification
import config from "./config";
import type {
  UserQueryInput,
  Soda,
  TransactionCustomer,
  AppResponse,
  UserActions,
} from "./types";

const API_BASE_URL = config.apiUrl;

export const api = {
  // POST /query/actions - for chat interactions
  sendUserQuery: async (
    customerId: number,
    query: string
  ): Promise<
    AppResponse<
      Array<
        | AppResponse<TransactionCustomer>
        | AppResponse<Array<TransactionCustomer>>
        | AppResponse<Soda>
        | AppResponse<string>
      >
    >
  > => {
    const requestBody: UserQueryInput = {
      customer_id: customerId,
      query: query,
    };

    const response = await fetch(
      `${API_BASE_URL}${config.endpoints.userQuery}`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(requestBody),
      }
    );

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  },

  // GET /soda - get all sodas for stock page
  getSodas: async (): Promise<Soda[]> => {
    const response = await fetch(`${API_BASE_URL}${config.endpoints.sodas}`);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    // Based on your OpenAPI spec, this returns the sodas directly
    const data = await response.json();
    return Array.isArray(data) ? data : data.data || [];
  },

  // GET /transaction/customer/{customer_id} - get transactions by customer
  getTransactionsByCustomer: async (
    customerId: number
  ): Promise<TransactionCustomer[]> => {
    const response = await fetch(
      `${API_BASE_URL}${config.endpoints.transactionsByCustomer}/${customerId}`
    );

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return Array.isArray(data) ? data : data.data || [];
  },
};

export default api;
