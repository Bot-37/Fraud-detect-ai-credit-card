
// This service will handle the interaction with the server.py API
// which connects to your fraud_detector.py

interface TransactionData {
    cardNumber: string;
    amount: number;
    cardholderName: string;
    transactionDate: string;
    [key: string]: any; // Allow for additional transaction data
  }
  
  interface FraudDetectionResponse {
    isFraudulent: boolean;
    score: number;
    reason?: string;
  }
  
  class FraudDetectionService {
    private apiUrl: string;
    
    constructor(apiUrl: string = 'http://localhost:5000/api/detect-fraud') {
      this.apiUrl = apiUrl;
    }
    
    async checkTransaction(transactionData: TransactionData): Promise<FraudDetectionResponse> {
      try {
        // In a real-world scenario, this would make an actual API call to your server.py
        // For now, we'll simulate with a mock response
        
        console.log('Sending transaction for fraud detection:', transactionData);
        
        // This is just a placeholder for the actual API call
        // const response = await fetch(this.apiUrl, {
        //   method: 'POST',
        //   headers: {
        //     'Content-Type': 'application/json',
        //   },
        //   body: JSON.stringify(transactionData),
        // });
        
        // if (!response.ok) {
        //   throw new Error(`Error: ${response.status}`);
        // }
        
        // const data = await response.json();
        // return data;
        
        // For now, returning a mock response
        return {
          isFraudulent: Math.random() < 0.1, // 10% chance of fraud detection for demo
          score: Math.random(),
          reason: Math.random() < 0.1 ? 'Unusual transaction amount' : undefined
        };
      } catch (error) {
        console.error('Error detecting fraud:', error);
        throw error;
      }
    }
    
    // This method will be used when you connect your actual fraud_detector.py
    setApiUrl(url: string): void {
      this.apiUrl = url;
    }
  }
  
  export const fraudDetectionService = new FraudDetectionService();
  export default fraudDetectionService;
  