# webportal/server.py
from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import joblib
import numpy as np
import pandas as pd
from datetime import datetime
import logging
from typing import Dict, List
from app.fraud_detector import FraudDetector  # Import your existing detector

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("FraudPortal")

# Initialize your FraudDetector
try:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(current_dir, '..', 'model', 'fraud_model.pkl')
    scaler_path = os.path.join(current_dir, '..', 'model', 'scaler.pkl')
    
    detector = FraudDetector(model_path=model_path, scaler_path=scaler_path)
    logger.info("✅ Fraud detection system initialized successfully")
except Exception as e:
    logger.error(f"❌ Failed to initialize fraud detector: {str(e)}")
    exit(1)

# Card database with enhanced details
valid_cards: Dict[str, Dict] = {
    # Valid cards with enhanced details
    '4111111111111111': {
        'name': 'John Smith',
        'limit': 5000,
        'issuer': 'Visa',
        'country': 'US',
        'expiry': '12/25'
    },
    '4222222222222222': {
        'name': 'Maria Garcia',
        'limit': 10000,
        'issuer': 'Mastercard',
        'country': 'ES',
        'expiry': '03/24'
    },
    # Add more cards with realistic details...
}

# Enhanced stolen card tracking
reported_stolen_cards: Dict[str, Dict] = {
    '4666666666666666': {
        'reported_date': '2023-05-15',
        'reported_by': 'Bank of America',
        'reason': 'Lost wallet'
    }
}

# Suspicious activity tracking
suspected_cards: Dict[str, Dict] = {}

def log_transaction(card_number: str, amount: float, status: str, reason: str):
    """Log transaction details for audit purposes"""
    logger.info(
        f"Transaction: {card_number[-4:]}, "
        f"Amount: {amount:.2f}, "
        f"Status: {status}, "
        f"Reason: {reason}"
    )

@app.route('/')
def index():
    """Main dashboard showing card status overview"""
    return render_template(
        'index.html',
        valid_cards=valid_cards,
        reported_cards=reported_stolen_cards,
        suspected_cards=suspected_cards,
        total_cards=len(valid_cards),
        stolen_count=len(reported_stolen_cards),
        suspected_count=len(suspected_cards)
    )

@app.route('/api/cards', methods=['GET'])
def get_cards_api():
    """API endpoint for card data"""
    return jsonify({
        'valid_cards': valid_cards,
        'reported_stolen': reported_stolen_cards,
        'suspected_cards': suspected_cards
    })

@app.route('/report_stolen', methods=['POST'])
def report_stolen():
    """Endpoint for reporting stolen cards with enhanced validation"""
    try:
        raw_card = request.form.get('card_number', '').strip()
        card_number = ''.join(filter(str.isdigit, raw_card))
        
        if not (13 <= len(card_number) <= 19):
            return "Invalid card number length", 400
            
        if card_number not in valid_cards:
            return "Card not in our system", 404
            
        if card_number in reported_stolen_cards:
            return "Card already reported", 409
            
        # Add reporting details
        reported_stolen_cards[card_number] = {
            'reported_date': datetime.now().strftime("%Y-%m-%d"),
            'reported_by': request.form.get('reporter_name', 'Customer'),
            'reason': request.form.get('reason', 'Not specified')
        }
        
        logger.warning(f"🚨 Card reported stolen: {card_number[-4:]}")
        return redirect(url_for('stolen_reported', card_number=card_number))
        
    except Exception as e:
        logger.error(f"Error reporting stolen card: {str(e)}")
        return "Internal server error", 500

@app.route('/check_transaction', methods=['POST'])
def check_transaction():
    """Enhanced transaction checking endpoint"""
    try:
        # Get and validate input
        card_number = request.form.get('card_number', '').strip()
        amount = float(request.form.get('amount', 0))
        
        if card_number not in valid_cards:
            return render_template('error.html', 
                                 message="Invalid card number"), 400
        
        # Check against stolen lists (immediate block)
        if card_number in reported_stolen_cards:
            log_transaction(card_number, amount, "BLOCKED", "Reported stolen")
            return render_template('result.html',
                                status="BLOCKED",
                                reason="Card reported stolen",
                                card_number=card_number,
                                amount=amount,
                                card_details=valid_cards[card_number],
                                stolen_details=reported_stolen_cards.get(card_number))
        
        # Create transaction data with proper features
        transaction = {
            'transaction_id': f"TX-{datetime.now().timestamp()}",
            'Amount': amount,
            **{f'V{i}': np.random.randn() for i in range(1, 29)}
        }
        
        # Use your existing detector for fraud detection
        detection_result = detector.detect_fraud(transaction)
        
        # Handle detection results
        if detection_result['is_fraud']:
            # Update suspected cards tracking
            if card_number not in suspected_cards:
                suspected_cards[card_number] = {
                    'first_detected': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'alert_count': 0,
                    'transactions': []
                }
            
            suspected_cards[card_number]['alert_count'] += 1
            suspected_cards[card_number]['last_alert'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            suspected_cards[card_number]['transactions'].append({
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'amount': amount,
                'confidence': detection_result['fraud_probability']
            })
            
            log_transaction(card_number, amount, "BLOCKED", 
                           f"Fraud detected (confidence: {detection_result['fraud_probability']:.2%})")
            
            return render_template('result.html',
                                status="BLOCKED",
                                reason=f"Fraud detected (confidence: {detection_result['fraud_probability']:.2%})",
                                card_number=card_number,
                                amount=amount,
                                card_details=valid_cards[card_number],
                                detection_details=detection_result)
        
        # Legitimate transaction
        log_transaction(card_number, amount, "APPROVED", "Legitimate transaction")
        return render_template('result.html',
                            status="APPROVED",
                            reason="Transaction appears legitimate",
                            card_number=card_number,
                            amount=amount,
                            card_details=valid_cards[card_number],
                            detection_details=detection_result)
    
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        return render_template('error.html', message=str(e)), 400
    except Exception as e:
        logger.error(f"Transaction check error: {str(e)}")
        return render_template('error.html', 
                            message="An error occurred processing your transaction"), 500

@app.route('/transaction_history')
def transaction_history():
    """Endpoint to view transaction history"""
    # Implement transaction history logic here
    pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)