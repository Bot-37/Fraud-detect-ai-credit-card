//services/fraudDetectionService.ts

export interface TransactionData {
  cardNumber: string;
  cardHolderName: string;
  amount: number;
  transactionDate: string;
  transactionType: string;
  merchantName: string;
  merchantCategory: string;
} 

export interface FraudCheckResult {
  isFraudulent: boolean;
  score: number;
  reason?: string;
}

export class FraudDetectionService {
  private apiUrl: string;

  constructor(apiUrl: string = 'http://localhost:5000/check-transaction') {
    this.apiUrl = apiUrl;
  }

  async checkTransaction(transactionData: TransactionData): Promise<FraudCheckResult> {
    try {
      const response = await fetch(this.apiUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-Correlation-ID': 'demo-correlation-id' // optional but good for logging
        },
        body: JSON.stringify({
          card_id: transactionData.cardNumber,
          amount: transactionData.amount,
          merchant_id: "M123456", // Optional: Replace with dynamic value if available
          timestamp: transactionData.transactionDate,
          location: {
            city: "Chennai",
            lat: 13.08,
            lon: 80.27
          },
          device_fingerprint: "device-abc-xyz",
          metadata: {}
        })
      });

      if (!response.ok) {
        throw new Error(`API Error: ${response.status} ${response.statusText}`);
      }

      const data = await response.json();

      return {
        isFraudulent: data.is_fraud,
        score: data.risk_score,
        reason: data.reasons?.join(', ') || 'No specific reason provided'
      };

    } catch (error) {
      console.error('Fraud detection API call failed:', error);
      throw error;
    }
  }
}
