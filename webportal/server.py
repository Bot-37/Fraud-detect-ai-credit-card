"""
Naan Mudhalvan Fraud Detection Portal Server
"""
import os
import json
import logging
from datetime import datetime
from typing import Dict, Any

from flask import (
    Flask, 
    render_template, 
    request, 
    redirect, 
    url_for, 
    session, 
    send_from_directory
)
import numpy as np

from app.fraud_detector import AdvancedFraudDetector

# --------------------------
# Application Configuration
# --------------------------

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', os.urandom(24))
app.config.update({
    'SESSION_TYPE': 'filesystem',
    'DATA_DIR': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data'),
    'MODEL_DIR': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'model'),
    'MAX_CART_ITEMS': 10,
    'SESSION_COOKIE_SECURE': True,
    'SESSION_COOKIE_HTTPONLY': True
})

# ----------------------
# Logging Configuration
# ----------------------

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join('logs', 'fraud_portal.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("FraudPortal")

# ---------------------
# Service Initialization
# ---------------------

try:
    fraud_detector = AdvancedFraudDetector(
        model_path=os.path.join(app.config['MODEL_DIR'], 'fraud_model.pkl'),
        scaler_path=os.path.join(app.config['MODEL_DIR'], 'scaler.pkl')
    )
    logger.info("Fraud detection system initialized successfully")
except Exception as e:
    logger.critical(f"Failed to initialize fraud detector: {str(e)}")
    raise RuntimeError("Critical system failure - fraud detector initialization") from e

# ---------------------
# Data Initialization
# ---------------------

class CardManager:
    """Manage card data and stolen card reporting"""
    
    def __init__(self):
        self.valid_cards = self._load_card_data()
        self.reported_cards: Dict[str, Dict] = {}
        self.suspected_cards: Dict[str, Dict] = {}
    
    @staticmethod
    def _load_card_data() -> Dict[str, Dict]:
        """Load and sanitize card data from JSON file"""
        try:
            cards_path = os.path.join(app.config['DATA_DIR'], 'fake_credit_card_dataset.json')
            with open(cards_path, 'r', encoding='utf-8') as f:
                return {
                    card['card_number'].replace(' ', '').strip(): {
                        'name': card['name'],
                        'limit': 1_000_000,
                        'issuer': card['card_type'],
                        'expiry': card['expiry_date'],
                        'cvv': card['cvv'],
                        'billing_address': card['billing_address'],
                        'fraudulent': card.get('fraudulent', False),
                        'id': card['id']
                    }
                    for card in json.load(f)
                }
        except Exception as e:
            logger.error(f"Card data loading failed: {str(e)}")
            raise RuntimeError("Card database initialization failed") from e

card_manager = CardManager()

# ---------------------
# Product Configuration
# ---------------------

PRODUCT_CATALOG = [
    {'id': 1, 'name': "iPhone 15 Pro", 'price': 119900, 
     'image': "/data/Iphone 15 Pro.png"},
    {'id': 2, 'name': "MacBook Air M3", 'price': 114900, 
     'image': "/data/MacBook Air M3.png"},
    {'id': 3, 'name': "Sony WH-1000XM5", 'price': 29990, 
     'image': "/data/Sony WH-1000XM5.png"},
    {'id': 4, 'name': "Samsung Galaxy Watch 6", 'price': 24999, 
     'image': "/data/Samsung Galaxy Watch 6.png"},
    {'id': 5, 'name': "iPad Air", 'price': 59900, 
     'image': "/data/Ipad Air.png"},
    {'id': 6, 'name': "Canon EOS R8", 'price': 189900, 
     'image': "/data/Canon EOS R8.png"},
    {'id': 7, 'name': "OnePlus 12", 'price': 64999, 
     'image': "/data/OnePlus.png"},
    {'id': 8, 'name': "Dell XPS 13", 'price': 109990, 
     'image': "/data/Dell XPS.png"}
]

# ---------------------
# Helper Functions
# ---------------------

def get_recent_transactions(card_number: str, hours: int = 1) -> int:
    """Mock recent transaction count for demo purposes"""
    return np.random.randint(0, 6)

def validate_card_number(card_number: str) -> bool:
    """Basic card number validation"""
    return 13 <= len(card_number) <= 19 and card_number.isdigit()

# ---------------------
# Route Definitions
# ---------------------

@app.route('/')
def dashboard():
    """Main fraud monitoring dashboard"""
    return render_template('demo.html',
                        valid_cards=card_manager.valid_cards,
                        reported_cards=card_manager.reported_cards,
                        suspected_cards=card_manager.suspected_cards)

@app.route('/shop')
def shopping_portal():
    """Display product catalog"""
    return render_template('demo.html', products=PRODUCT_CATALOG)

@app.route('/cart')
def view_cart():
    """Display shopping cart contents"""
    cart = session.get('cart', {})
    return render_template('success.html',
                        cart=cart.values(),
                        total=sum(item['price'] * item['quantity'] for item in cart.values()))

@app.route('/checkout', methods=['POST'])
def process_checkout():
    """Process transaction with fraud checks"""
    try:
        # Extract and validate payment details
        card_number = request.form.get('card_number', '').replace(' ', '')
        card_data = card_manager.valid_cards.get(card_number)
        
        if not card_data:
            return render_template('failed.html', 
                                message="Invalid card number"), 400
        
        if card_data.get('fraudulent', False):
            return render_template('flagged.html',
                                card_number=card_number,
                                reason="Permanently flagged as fraudulent")

        # Process transaction
        cart = session.get('cart', {})
        if not cart:
            return redirect(url_for('shopping_portal'))

        transaction_data = {
            'amount': sum(item['price'] * item['quantity'] for item in cart.values()),
            'cvv': request.form.get('cvv', ''),
            'merchant_location': (19.0760, 72.8777),
            'transaction_time': datetime.utcnow().isoformat(),
            'merchant_category': 'electronics',
            'hourly_count': get_recent_transactions(card_number)
        }

        fraud_result = fraud_detector.process_transaction(card_data, transaction_data)
        
        if fraud_result['final_verdict']:
            return render_template('flagged.html',
                                detection_result=fraud_result,
                                card_number=card_number,
                                total_amount=transaction_data['amount'])
        session.pop('cart', None)
        return render_template('success.html',
                            transaction_id=f"ORD-{datetime.now():%Y%m%d%H%M%S}",
                            card_number=card_number,
                            amount=transaction_data['amount'])

    except Exception as e:
        logger.error(f"Checkout error: {str(e)}")
        return render_template('failed.html',
                            message="Transaction processing failed"), 500

@app.route('/report_stolen', methods=['GET', 'POST'])
def report_stolen_card():
    """Handle stolen card reporting"""
    if request.method == 'GET':
        return render_template('report_stolen.html')
    
    try:
        card_number = ''.join(filter(str.isdigit, request.form.get('card_number', '')))
        
        if not validate_card_number(card_number):
            return render_template('failed.html',
                                message="Invalid card number"), 400
        
        if card_number in card_manager.reported_cards:
            return render_template('failed.html',
                                message="Card already reported"), 409
            
        card_manager.reported_cards[card_number] = {
            'reported_date': datetime.now().strftime("%Y-%m-%d"),
            'reported_by': request.form.get('reporter_name', 'Customer'),
            'reason': request.form.get('reason', 'Not specified')
        }
        return redirect(url_for('stolen_card_confirmation', card_number=card_number))
    
    except Exception as e:
        logger.error(f"Stolen report error: {str(e)}")
        return render_template('failed.html',
                            message="Failed to process report"), 500

# ---------------------
# Utility Routes
# ---------------------

@app.route('/data/<path:filename>')
def serve_image(filename):
    """Serve product images"""
    return send_from_directory(app.config['DATA_DIR'], filename)

@app.route('/stolen_reported/<card_number>')
def stolen_card_confirmation(card_number: str):
    """Display stolen card report confirmation"""
    return render_template('stolen_reported.html',
                        card_number=card_number,
                        card_details=card_manager.valid_cards.get(card_number, {}),
                        stolen_details=card_manager.reported_cards.get(card_number, {}))

# ---------------------
# Error Handlers
# ---------------------

@app.errorhandler(404)
def page_not_found(e):
    return render_template('failed.html',
                        message="Requested resource not found"), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('failed.html',
                        message="Internal server error"), 500
