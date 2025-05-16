export interface TransactionData {
  amount: number;
  transactionDate: string;  // Renamed from `time` to match the form
  cardNumber: string;       // Renamed from `card_number` to match the form
  cardHolderName: string;   // Renamed from `card_Holdername` to match the form
  merchantId: string;       // Matches the form
  transactionType: string;  // Renamed from `card_type` to match the form
  location?: string;        // Optional: Add if needed
  userId?: string;          // Optional: Add if needed
  transactionId?: string;   // Optional: Add if needed
  merchantName: string;
  merchantCategory: string;
}

export interface FraudCheckResult {
  prediction: number;    // 0 or 1 from your model
  probability: number;   // float probability of fraud
}

export class FraudDetectionService {
  private apiUrl: string;

  constructor(apiUrl: string = '/api/predict') {  // <-- use proxy path here
    this.apiUrl = apiUrl;
  }

  async checkTransaction(transactionData: TransactionData): Promise<FraudCheckResult> {
    try {
      const response = await fetch(this.apiUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-Correlation-ID': 'demo-correlation-id' // optional for tracing logs
        },
        body: JSON.stringify(transactionData),  // payload keys exactly match FastAPI schema
      });

      if (!response.ok) {
        throw new Error(`API Error: ${response.status} ${response.statusText}`);
      }

      const data = await response.json();

      // The backend returns keys: fraud_prediction and fraud_probability
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
