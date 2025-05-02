import json
import numpy as np
from datetime import datetime, timedelta

def generate_transactions(num=50):
    transactions = []
    for i in range(num):
        # Generate random values with some patterns that might indicate fraud
        is_fraud = np.random.choice([0, 1], p=[0.9, 0.1])
        
        if is_fraud:
            # Patterns that might indicate fraud
            amount = np.random.uniform(100, 5000)
            v_values = np.random.uniform(-3, 3, 28)
            v_values[0] = abs(v_values[0]) * 2  # V1 often higher for fraud
            v_values[14] = -abs(v_values[14]) * 2  # V14 often lower for fraud
        else:
            # Normal transaction patterns
            amount = np.random.uniform(10, 500)
            v_values = np.random.uniform(-1, 1, 28)
        
        transaction = {
            "transaction_id": f"TX{10000 + i}",
            "timestamp": (datetime.now() - timedelta(minutes=np.random.randint(0, 1440))).isoformat(),
            "Amount": float(amount),
            **{f"V{i+1}": float(v_values[i]) for i in range(28)}
        }
        transactions.append(transaction)
    
    return transactions

# Generate and save test data
test_data = generate_transactions(50)

# Save as individual JSON files
for i, tx in enumerate(test_data, 1):
    with open(f'test_data/transaction_{i}.json', 'w') as f:
        json.dump(tx, f, indent=2)

# Save as single combined file
with open('test_data/all_transactions.json', 'w') as f:
    json.dump(test_data, f, indent=2)

print("Generated 50 test transactions in test_data/ directory")