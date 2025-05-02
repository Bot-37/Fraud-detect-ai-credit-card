# webportal/server.py
from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
import os
import json
import joblib
import numpy as np
import pandas as pd
from datetime import datetime
import logging
from typing import Dict, List
from app.fraud_detector import FraudDetector

# Initialize Flask application
app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SESSION_TYPE'] = 'filesystem'

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("FraudPortal")

# Configure paths
current_dir = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(current_dir, '..', 'data')
MODEL_DIR = os.path.join(current_dir, '..', 'model')

# Initialize FraudDetector
try:
    detector = FraudDetector(
        model_path=os.path.join(MODEL_DIR, 'fraud_model.pkl'),
        scaler_path=os.path.join(MODEL_DIR, 'scaler.pkl')
    )
    logger.info("✅ Fraud detection system initialized successfully")
except Exception as e:
    logger.error(f"❌ Failed to initialize fraud detector: {str(e)}")
    exit(1)

# Product data (unchanged)
PRODUCTS = [
    {'id': 1, 'name': "iPhone 15 Pro", 'price': 119900, 'image': "Iphone 15 Pro.png"},
    {'id': 2, 'name': "MacBook Air M3", 'price': 114900, 'image': "MacBook Air M3.png"},
    {'id': 3, 'name': "Sony WH-1000XM5", 'price': 29990, 'image': "Sony WH-1000XM5.png"},
    {'id': 4, 'name': "Samsung Galaxy Watch 6", 'price': 24999, 'image': "Samsung Galaxy Watch 6.png"},
    {'id': 5, 'name': "iPad Air", 'price': 59900, 'image': "Ipad Air.png"},
    {'id': 6, 'name': "Canon EOS R8", 'price': 189900, 'image': "Canon EOS R8.png"},
    {'id': 7, 'name': "OnePlus 12", 'price': 64999, 'image': "OnePlus.png"},
    {'id': 8, 'name': "Dell XPS 13", 'price': 109990, 'image': "Dell XPS.png"}
]

# Card database loading from JSON
def load_card_data():
    """Load and sanitize card data from JSON file"""
    try:
        cards_path = os.path.join(DATA_DIR, 'fake_credit_card_dataset.json')
        with open(cards_path, 'r') as f:
            raw_cards = json.load(f)
        
        valid_cards = {}
        for card in raw_cards:
            # Sanitize card number
            clean_number = card['card_number'].replace(' ', '').strip()
            
            valid_cards[clean_number] = {
                'name': card['name'],
                'limit': 1000000,  # Default limit, adjust as needed
                'issuer': card['card_type'],
                'country': 'IN',  # Extract from address if available
                'expiry': card['expiry_date'],
                'cvv': card['cvv'],
                'billing_address': card['billing_address']
            }
        return valid_cards
    except Exception as e:
        logger.error(f"❌ Failed to load card data: {str(e)}")
        exit(1)

valid_cards = load_card_data()
reported_stolen_cards: Dict[str, Dict] = {}
suspected_cards: Dict[str, Dict] = {}

@app.route('/data/<path:filename>')
def serve_data(filename):
    """Serve files from the data directory"""
    return send_from_directory(DATA_DIR, filename)

def log_transaction(card_number: str, amount: float, status: str, reason: str):
    """Log transaction details"""
    logger.info(
        f"Transaction: {card_number[-4:]}, "
        f"Amount: ₹{amount:,.2f}, "
        f"Status: {status}, "
        f"Reason: {reason}"
    )

# Shopping Interface Routes
@app.route('/demo')
def shopping_portal():
    """Shopping interface"""
    cart = session.get('cart', {})
    cart_total = sum(item['price'] * item['quantity'] for item in cart.values())
    return render_template('demo.html',
                         products=PRODUCTS,
                         cart=cart,
                         cart_total=cart_total)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    """Add item to cart"""
    product_id = request.form.get('product_id')
    product = next((p for p in PRODUCTS if str(p['id']) == product_id), None)
    
    if product:
        cart = session.get('cart', {})
        cart_key = str(product['id'])
        cart[cart_key] = {
            'name': product['name'],
            'price': product['price'],
            'quantity': cart.get(cart_key, {'quantity': 0})['quantity'] + 1,
            'image': product['image']
        }
        session['cart'] = cart
    return redirect(url_for('shopping_portal'))

@app.route('/update_cart', methods=['POST'])
def update_cart():
    """Modify cart contents"""
    product_id = request.form.get('product_id')
    action = request.form.get('action')
    
    cart = session.get('cart', {})
    if product_id in cart:
        if action == 'increase':
            cart[product_id]['quantity'] += 1
        elif action == 'decrease' and cart[product_id]['quantity'] > 1:
            cart[product_id]['quantity'] -= 1
        elif action == 'remove':
            del cart[product_id]
    
    session['cart'] = cart
    return redirect(url_for('shopping_portal'))

@app.route('/checkout', methods=['POST'])
def process_checkout():
    """Handle checkout process"""
    try:
        card_number = request.form.get('card_number', '').replace(' ', '')
        card_name = request.form.get('card_name', '')
        expiry = request.form.get('expiry', '')
        cvv = request.form.get('cvv', '')
        
        if not all([card_number, card_name, expiry, cvv]):
            return render_template('error.html', message="All fields are required"), 400

        cart = session.get('cart', {})
        if not cart:
            return redirect(url_for('shopping_portal'))
            
        total_amount = sum(item['price'] * item['quantity'] for item in cart.values())
        
        if card_number in reported_stolen_cards:
            return render_template('blocked.html',
                                card_number=card_number,
                                details=reported_stolen_cards[card_number])
        
        transaction = {
            'transaction_id': f"TX-{datetime.now().timestamp()}",
            'Amount': total_amount,
            **{f'V{i}': np.random.randn() for i in range(1, 29)}
        }
        
        detection_result = detector.detect_fraud(transaction)
        
        if detection_result['is_fraud']:
            suspected_cards[card_number] = {
                'first_detected': datetime.now().isoformat(),
                'transactions': [transaction]
            }
            return render_template('checkout_result.html',
                                detection_result=detection_result,
                                card_number=card_number,
                                total_amount=total_amount)
        else:
            transaction_id = f"ORD-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            session.pop('cart', None)
            return render_template('success.html',
                                transaction_id=transaction_id,
                                card_number=card_number,
                                total_amount=total_amount,
                                cart_items=cart.values())

    except Exception as e:
        logger.error(f"Checkout error: {str(e)}")
        return render_template('error.html',
                            message="An error occurred during checkout"), 500

# Fraud Management Routes
@app.route('/report_stolen', methods=['POST'])
def report_stolen_card():
    """Handle stolen card reports"""
    try:
        raw_card = request.form.get('card_number', '').strip()
        card_number = ''.join(filter(str.isdigit, raw_card))
        
        if not 13 <= len(card_number) <= 19:
            return "Invalid card number length", 400
            
        if card_number not in valid_cards:
            return "Card not in our system", 404
            
        if card_number in reported_stolen_cards:
            return "Card already reported", 409
            
        reported_stolen_cards[card_number] = {
            'reported_date': datetime.now().strftime("%Y-%m-%d"),
            'reported_by': request.form.get('reporter_name', 'Customer'),
            'reason': request.form.get('reason', 'Not specified')
        }
        
        logger.warning(f"🚨 Card reported stolen: {card_number[-4:]}")
        return redirect(url_for('stolen_card_confirmation', card_number=card_number))
        
    except Exception as e:
        logger.error(f"Error reporting card: {str(e)}")
        return "Internal server error", 500

@app.route('/stolen_reported/<card_number>')
def stolen_card_confirmation(card_number: str):
    """Show stolen card report confirmation"""
    return render_template('stolen_reported.html',
                         card_number=card_number,
                         card_details=valid_cards.get(card_number, {}),
                         stolen_details=reported_stolen_cards.get(card_number, {}))

# Main Dashboard
@app.route('/')
def fraud_dashboard():
    """Main fraud monitoring dashboard"""
    return render_template('index.html',
                         valid_cards=valid_cards,
                         reported_cards=reported_stolen_cards,
                         suspected_cards=suspected_cards,
                         total_cards=len(valid_cards),
                         stolen_count=len(reported_stolen_cards),
                         suspected_count=len(suspected_cards))