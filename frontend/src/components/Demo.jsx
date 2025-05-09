import { useState, useEffect } from 'react';

// Sample product data
const products = [
  { id: 1, name: "iPhone 15 Pro", price: 119900, image: "/data/Iphone 15 Pro.png" },
  { id: 2, name: "MacBook Air M3", price: 114900, image: "/data/MacBook Air M3.png" },
  { id: 3, name: "Sony WH-1000XM5", price: 29990, image: "/data/Sony WH-1000XM5.png" },
  { id: 4, name: "Samsung Galaxy Watch 6", price: 24999, image: "/data/Samsung Galaxy Watch 6.png" },
  { id: 5, name: "iPad Air", price: 59900, image: "/data/Ipad Air.png" },
  { id: 6, name: "Canon EOS R8", price: 189900, image: "/data/Canon EOS R8.png" },
  { id: 7, name: "OnePlus 12", price: 64999, image: "/data/OnePlus.png" },
  { id: 8, name: "Dell XPS 13", price: 109990, image: "/data/Dell XPS.png" }
];

// Format price to Indian Rupees
const formatPrice = (price) => {
  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    maximumFractionDigits: 0
  }).format(price);
}

// Product Card Component
const ProductCard = ({ product, addToCart }) => {
  return (
    <div className="bg-gray-800 rounded-xl overflow-hidden shadow-lg transition-all duration-300 hover:translate-y-1 hover:shadow-xl">
      <div className="h-48 bg-gray-700 relative overflow-hidden">
        <img 
          src={product.image} 
          alt={product.name}
          className="w-full h-full object-cover transition-transform duration-500 hover:scale-105"
        />
      </div>
      <div className="p-5">
        <h3 className="text-lg font-semibold mb-2 text-gray-200">{product.name}</h3>
        <div className="text-xl font-bold mb-4 text-indigo-300">{formatPrice(product.price)}</div>
        <button 
          className="w-full bg-indigo-500 text-white font-medium py-2 px-5 rounded-lg hover:bg-indigo-600 transition-colors duration-300"
          onClick={() => addToCart(product.id)}
        >
          Add to Cart
        </button>
      </div>
    </div>
  );
}

// Cart Item Component
const CartItem = ({ item, increaseQuantity, decreaseQuantity }) => {
  const itemTotal = item.price * item.quantity;
  
  return (
    <div className="flex justify-between items-center py-3 border-b border-gray-700 text-gray-200">
      <div className="flex-1">{item.name}</div>
      <div className="flex items-center gap-2 mr-4">
        <button 
          className="w-6 h-6 flex items-center justify-center bg-gray-700 text-gray-200 rounded hover:bg-indigo-500 transition-colors"
          onClick={() => decreaseQuantity(item.id)}
        >
          -
        </button>
        <span className="w-5 text-center">{item.quantity}</span>
        <button 
          className="w-6 h-6 flex items-center justify-center bg-gray-700 text-gray-200 rounded hover:bg-indigo-500 transition-colors"
          onClick={() => increaseQuantity(item.id)}
        >
          +
        </button>
      </div>
      <span className="font-medium">{formatPrice(itemTotal)}</span>
    </div>
  );
}

// Checkout Form Component
const CheckoutForm = ({ processPayment }) => {
  const [formData, setFormData] = useState({
    cardName: '',
    cardNumber: '',
    cardExpiry: '',
    cardCvv: ''
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.id]: e.target.value
    });
  };

  return (
    <div className="bg-gray-800 rounded-xl shadow-lg p-6">
      <h3 className="text-xl font-semibold mb-6 text-gray-200">Payment Information</h3>
      <div className="mb-5">
        <label htmlFor="cardName" className="block mb-2 font-medium text-sm text-gray-200">
          Cardholder Name
        </label>
        <input
          type="text"
          id="cardName"
          className="w-full py-3 px-4 text-base bg-gray-700 border border-gray-600 text-gray-200 rounded-lg transition-all focus:outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20"
          placeholder="Enter cardholder name"
          value={formData.cardName}
          onChange={handleChange}
          required
        />
      </div>
      <div className="mb-5">
        <label htmlFor="cardNumber" className="block mb-2 font-medium text-sm text-gray-200">
          Card Number
        </label>
        <input
          type="text"
          id="cardNumber"
          className="w-full py-3 px-4 text-base bg-gray-700 border border-gray-600 text-gray-200 rounded-lg transition-all focus:outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20"
          placeholder="1234 5678 9012 3456"
          value={formData.cardNumber}
          onChange={handleChange}
          required
        />
      </div>
      <div className="mb-5">
        <label htmlFor="cardExpiry" className="block mb-2 font-medium text-sm text-gray-200">
          Expiration Date
        </label>
        <input
          type="text"
          id="cardExpiry"
          className="w-full py-3 px-4 text-base bg-gray-700 border border-gray-600 text-gray-200 rounded-lg transition-all focus:outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20"
          placeholder="MM/YY"
          value={formData.cardExpiry}
          onChange={handleChange}
          required
        />
      </div>
      <div className="mb-5">
        <label htmlFor="cardCvv" className="block mb-2 font-medium text-sm text-gray-200">
          CVV
        </label>
        <input
          type="text"
          id="cardCvv"
          className="w-full py-3 px-4 text-base bg-gray-700 border border-gray-600 text-gray-200 rounded-lg transition-all focus:outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20"
          placeholder="123"
          value={formData.cardCvv}
          onChange={handleChange}
          required
        />
      </div>
      <button 
        className="w-full bg-green-500 text-white font-semibold py-3 px-4 text-base rounded-lg hover:bg-green-600 transition-colors"
        onClick={() => processPayment(formData)}
      >
        Process Payment
      </button>
    </div>
  );
}

// Main App Component
export default function App() {
  const [cart, setCart] = useState([]);
  const [total, setTotal] = useState(0);

  // Calculate cart total whenever cart changes
  useEffect(() => {
    const newTotal = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    setTotal(newTotal);
  }, [cart]);

  // Add item to cart
  const addToCart = (productId) => {
    const product = products.find(p => p.id === productId);
    if (product) {
      setCart(prevCart => {
        const existingItem = prevCart.find(item => item.id === productId);
        if (existingItem) {
          return prevCart.map(item => 
            item.id === productId 
              ? { ...item, quantity: item.quantity + 1 } 
              : item
          );
        } else {
          return [...prevCart, { ...product, quantity: 1 }];
        }
      });
    }
  };

  // Decrease quantity or remove item
  const decreaseQuantity = (productId) => {
    setCart(prevCart => {
      const existingItem = prevCart.find(item => item.id === productId);
      if (existingItem && existingItem.quantity > 1) {
        return prevCart.map(item => 
          item.id === productId 
            ? { ...item, quantity: item.quantity - 1 } 
            : item
        );
      } else {
        return prevCart.filter(item => item.id !== productId);
      }
    });
  };

  // Process payment
  const processPayment = (formData) => {
    const { cardNumber } = formData;
    
    if (!cardNumber || cart.length === 0) {
      // Redirect to failed page in a real app
      alert("Payment failed. Please check your card details or cart.");
      return;
    }
    
    const isFraudulent = simulateFraudDetection(cardNumber, total);
    
    if (isFraudulent) {
      // Redirect to flagged page in a real app
      alert("This transaction has been flagged as potentially fraudulent.");
    } else {
      // Redirect to success page in a real app
      alert("Payment successful! Thank you for your purchase.");
      setCart([]);
    }
  };

  // Simple fraud detection logic
  const simulateFraudDetection = (cardNumber, amount) => {
    if (cardNumber.endsWith('1111')) return true;
    if (amount > 250000) return true;
    if (cart.length > 5 && amount > 100000) return true;
    return false;
  };

  return (
    <div className="min-h-screen bg-gray-900 text-gray-200">
      <header className="bg-gray-800 border-b border-gray-700 py-5 px-8 shadow-md">
        <div className="max-w-6xl mx-auto">
          <div className="flex items-center gap-4">
            <div className="w-36 h-24 bg-white rounded-lg flex items-center justify-center overflow-hidden">
              <img src="/data/image.png" alt="Naan Mudhalavan Logo" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-gray-200">Naan Mudhalavan Shopping</h1>
              <p className="text-sm text-gray-400 mt-0.5">Smart Shopping with Fraud Protection</p>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-6xl mx-auto py-8 px-6">
        <h2 className="text-2xl font-semibold mb-6 text-gray-200 relative pb-2 after:content-[''] after:absolute after:bottom-0 after:left-0 after:w-16 after:h-0.5 after:bg-indigo-500 after:rounded">
          Featured Electronics
        </h2>
        
        {/* Products Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8 mb-12">
          {products.map(product => (
            <ProductCard 
              key={product.id} 
              product={product} 
              addToCart={addToCart} 
            />
          ))}
        </div>

        {/* Cart and Checkout */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {/* Shopping Cart */}
          <div className="bg-gray-800 rounded-xl shadow-lg p-6">
            <h3 className="text-xl font-semibold mb-5 pb-3 border-b border-gray-700 text-gray-200">
              Your Shopping Cart
            </h3>
            <div>
              {cart.length === 0 ? (
                <div className="py-3 text-gray-400 italic">
                  Your cart is empty
                </div>
              ) : (
                cart.map(item => (
                  <CartItem 
                    key={item.id} 
                    item={item} 
                    increaseQuantity={addToCart}
                    decreaseQuantity={decreaseQuantity}
                  />
                ))
              )}
            </div>
            <div className="flex justify-between font-semibold text-lg pt-4 mt-2 text-gray-200">
              <span>Total:</span>
              <span>{formatPrice(total)}</span>
            </div>
          </div>

          {/* Checkout Form */}
          <CheckoutForm processPayment={processPayment} />
        </div>
      </main>
    </div>
  );
}