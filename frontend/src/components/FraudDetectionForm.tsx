import React, { useState } from "react";
import { TransactionData, FraudCheckResult, FraudDetectionService } from "../serivces/fraudDetectionService";

const fraudDetectionService = new FraudDetectionService();

const FraudDetectionForm: React.FC = () => {
  const [formData, setFormData] = useState<TransactionData>({
    cardNumber: "",
    cardHolderName: "",
    amount: 0,
    transactionDate: "",
    transactionType: "",
    merchantName: "",
    merchantCategory: "",
  });

  const [result, setResult] = useState<FraudCheckResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({ ...prevData, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setResult(null);

    try {
      const predictionResult = await fraudDetectionService.checkTransaction(formData);
      setResult(predictionResult);
    } catch (err: any) {
      setError(err.message);
    }
  };

  return (
    <div className="max-w-xl mx-auto p-6 bg-white shadow rounded-lg">
      <h2 className="text-lg font-bold mb-4">Fraud Detection Form</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700">Card Number</label>
          <input
            type="text"
            name="cardNumber"
            value={formData.cardNumber}
            onChange={handleChange}
            className="mt-1 block w-full border-gray-300 rounded-md"
            required
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">Card Holder Name</label>
          <input
            type="text"
            name="cardHolderName"
            value={formData.cardHolderName}
            onChange={handleChange}
            className="mt-1 block w-full border-gray-300 rounded-md"
            required
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">Transaction Amount</label>
          <input
            type="number"
            name="amount"
            value={formData.amount}
            onChange={handleChange}
            className="mt-1 block w-full border-gray-300 rounded-md"
            required
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">Transaction Date</label>
          <input
            type="datetime-local"
            name="transactionDate"
            value={formData.transactionDate}
            onChange={handleChange}
            className="mt-1 block w-full border-gray-300 rounded-md"
            required
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">Transaction Type</label>
          <select
            name="transactionType"
            value={formData.transactionType}
            onChange={handleChange}
            className="mt-1 block w-full border-gray-300 rounded-md"
            required
          >
            <option value="">Select</option>
            <option value="purchase">Purchase</option>
            <option value="refund">Refund</option>
            <option value="withdrawal">Withdrawal</option>
          </select>
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">Merchant Name</label>
          <input
            type="text"
            name="merchantName"
            value={formData.merchantName}
            onChange={handleChange}
            className="mt-1 block w-full border-gray-300 rounded-md"
            required
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">Merchant Category</label>
          <input
            type="text"
            name="merchantCategory"
            value={formData.merchantCategory}
            onChange={handleChange}
            className="mt-1 block w-full border-gray-300 rounded-md"
            required
          />
        </div>
        <button
          type="submit"
          className="w-full bg-brand-DEFAULT text-white py-2 px-4 rounded-md hover:bg-brand-dark"
        >
          Check Fraud
        </button>
      </form>

      {result && (
        <div className="mt-6 p-4 bg-green-50 border border-green-200 rounded-lg">
          <h3 className="text-lg font-bold text-green-700">Fraud Detection Result</h3>
          <p className="text-green-700">
            <strong>Fraudulent:</strong> {result.isFraudulent ? "Yes" : "No"}
          </p>
          <p className="text-green-700">
            <strong>Risk Score:</strong> {result.score}
          </p>
          <p className="text-green-700">
            <strong>Reason:</strong> {result.reason || "No specific reason provided"}
          </p>
        </div>
      )}

      {error && (
        <div className="mt-6 p-4 bg-red-50 border border-red-200 rounded-lg">
          <h3 className="text-lg font-bold text-red-600">Error</h3>
          <p className="text-red-600">{error}</p>
        </div>
      )}
    </div>
  );
};

export default FraudDetectionForm;