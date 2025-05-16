export interface TransactionData {
  amount: number;
  transactionDate: string;
  cardNumber: string;
  cardHolderName: string;
  merchantId: string;
  transactionType: string;
  location?: string;
  userId?: string;
  transactionId?: string;
  merchantName: string;
  merchantCategory: string;
}

export interface FraudCheckResult {
  prediction: number; // 0 or 1 from your model
  probability: number; // float probability of fraud
}

export class FraudDetectionService {
  private apiUrl: string;

  constructor(apiUrl: string = '/api/predict') {
    this.apiUrl = apiUrl;
  }

  async checkTransaction(transactionData: TransactionData): Promise<FraudCheckResult> {
    try {
      const formattedData = {
        amount: transactionData.amount,
        time: transactionData.transactionDate,
        card_number: transactionData.cardNumber,
        merchant_id: transactionData.merchantId,
        card_type: transactionData.transactionType,
        location: transactionData.location,
        user_id: transactionData.userId,
        transaction_id: transactionData.transactionId,
        card_holder_name: transactionData.cardHolderName,
        merchant_name: transactionData.merchantName,
        merchant_category: transactionData.merchantCategory,
      };

      const response = await fetch(this.apiUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer fake-jwt-token-demo-only',  // ✅ <-- Add this line
          'X-Correlation-ID': 'demo-correlation-id',
        },
        body: JSON.stringify(formattedData),
      });
      

      // Check if the response is OK
      if (!response.ok) {
        const errorText = await response.text();
        let errorData;
        try {
          errorData = JSON.parse(errorText); // Attempt to parse the error response as JSON
        } catch {
          throw new Error(`Backend Error: ${response.status} ${response.statusText}`);
        }
        throw new Error(errorData.detail || `API Error: ${response.status} ${response.statusText}`);
      }

      // Handle the response body
      const text = await response.text();
      if (!text) {
        throw new Error('Backend returned an empty response');
      }

      let data;
      try {
        data = JSON.parse(text); // Parse JSON response
      } catch {
        throw new Error('Failed to parse JSON from backend response');
      }

      // Validate and return the result
      if (
        !data.data ||
        typeof data.data.fraud_prediction === 'undefined' ||
        typeof data.data.fraud_probability === 'undefined'
      ) {
        throw new Error('Invalid response structure from backend');
      }

      return {
        prediction: data.data.fraud_prediction,
        probability: data.data.fraud_probability,
      };
    } catch (error) {
      console.error('Fraud detection API call failed:', error);
      throw error;
    }
  }
}