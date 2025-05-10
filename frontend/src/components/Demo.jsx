import { useState, useEffect } from 'react';

// Sample product data
const products = [
  { id: 1, name: "iPhone 15 Pro", price: 119900, image: "/public/product/Iphone 15 Pro.png" },
  { id: 2, name: "MacBook Air M3", price: 114900, image: "/public/product/MacBook Air M3.png" },
  { id: 3, name: "Sony WH-1000XM5", price: 29990, image: "/public/product/Sony WH-1000XM5.png" },
  { id: 4, name: "Samsung Galaxy Watch 6", price: 24999, image: "/public/product/Samsung Galaxy Watch 6.png" },
  { id: 5, name: "iPad Air", price: 59900, image: "/public/product/Ipad Air.png" },
  { id: 6, name: "Canon EOS R8", price: 189900, image: "/public/product/Canon EOS R8.png" },
  { id: 7, name: "OnePlus 12", price: 64999, image: "/public/product/OnePlus.png" },
  { id: 8, name: "Dell XPS 13", price: 109990, image: "/public/product/Dell XPS.png" }
];

// Format price to Indian Rupees
const formatPrice = (price) => {
  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    maximumFractionDigits: 0
  }).format(price);
}

// Product Card
const ProductCard = ({ product, addToCart }) => (
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

// Cart Item
const CartItem = ({ item, increaseQuantity, decreaseQuantity }) => {
  const itemTotal = item.price * item.quantity;
  return (
    <div className="flex justify-between items-center py-3 border-b border-gray-700 text-gray-200">
      <div className="flex-1">{item.name}</div>
      <div className="flex items-center gap-2 mr-4">
        <button 
          className="w-6 h-6 flex items-center justify-center bg-gray-700 text-gray-200 rounded hover:bg-indigo-500 transition-colors"
          onClick={() => decreaseQuantity(item.id)}
        >-</button>
        <span className="w-5 text-center">{item.quantity}</span>
        <button 
          className="w-6 h-6 flex items-center justify-center bg-gray-700 text-gray-200 rounded hover:bg-indigo-500 transition-colors"
          onClick={() => increaseQuantity(item.id)}
        >+</button>
      </div>
      <span className="font-medium">{formatPrice(itemTotal)}</span>
    </div>
  );
};

// Checkout Form
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

      {["cardName", "cardNumber", "cardExpiry", "cardCvv"].map(field => (
        <div className="mb-5" key={field}>
          <label htmlFor={field} className="block mb-2 font-medium text-sm text-gray-200">
            {field === 'cardName' ? 'Cardholder Name' :
             field === 'cardNumber' ? 'Card Number' :
             field === 'cardExpiry' ? 'Expiration Date' :
             'CVV'}
          </label>
          <input
            type="text"
            id={field}
            placeholder={
              field === 'cardName' ? 'Enter cardholder name' :
              field === 'cardNumber' ? '1234 5678 9012 3456' :
              field === 'cardExpiry' ? 'MM/YY' : '123'
            }
            className="w-full py-3 px-4 text-base bg-gray-700 border border-gray-600 text-gray-200 rounded-lg focus:outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20"
            value={formData[field]}
            onChange={handleChange}
            required
          />
        </div>
      ))}

      <button 
        className="w-full bg-green-500 text-white font-semibold py-3 px-4 text-base rounded-lg hover:bg-green-600 transition-colors"
        onClick={() => processPayment(formData)}
      >
        Process Payment
      </button>
    </div>
  );
};

// Main App
export default function App() {
  const [cart, setCart] = useState([]);
  const [total, setTotal] = useState(0);

  // Recalculate total on cart change
  useEffect(() => {
    const newTotal = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    setTotal(newTotal);
  }, [cart]);

  // Add item to cart
  const addToCart = (productId) => {
    const product = products.find(p => p.id === productId);
    if (product) {
      setCart(prev => {
        const exists = prev.find(item => item.id === productId);
        return exists
          ? prev.map(item => item.id === productId ? { ...item, quantity: item.quantity + 1 } : item)
          : [...prev, { ...product, quantity: 1 }];
      });
    }
  };

  // Decrease or remove item
  const decreaseQuantity = (productId) => {
    setCart(prev => {
      const item = prev.find(i => i.id === productId);
      return item.quantity > 1
        ? prev.map(i => i.id === productId ? { ...i, quantity: i.quantity - 1 } : i)
        : prev.filter(i => i.id !== productId);
    });
  };

  // Increase quantity
  const increaseQuantity = (productId) => {
    setCart(prev => prev.map(item => item.id === productId ? { ...item, quantity: item.quantity + 1 } : item));
  };

  // Simulate fraud detection (placeholder logic)
  const isFraudulentCard = (cardNumber) => {
    // Simple mock: if card number ends with '0000', treat as fraud
    return cardNumber.endsWith("0000");
  };

  // Handle payment processing
  const processPayment = (formData) => {
    if (!formData.cardNumber || cart.length === 0) {
      alert("❌ Payment failed. Check your card details or cart.");
      return;
    }

    if (isFraudulentCard(formData.cardNumber)) {
      alert("🚨 Payment flagged as fraudulent! Transaction declined.");
    } else {
      alert(`✅ Payment successful! Total: ${formatPrice(total)}`);
      setCart([]); // Clear cart on success
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 p-6 text-white">
      <h1 className="text-3xl font-bold text-center mb-6">Naan Mudhalavan Shopping</h1>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="md:col-span-2 grid grid-cols-1 sm:grid-cols-2 gap-6">
          {products.map(product => (
            <ProductCard key={product.id} product={product} addToCart={addToCart} />
          ))}
        </div>

        <div className="space-y-6">
          <div className="bg-gray-800 rounded-xl p-4 shadow-lg">
            <h2 className="text-xl font-semibold mb-4">🛍️ Cart</h2>
            {cart.length === 0 ? (
              <p className="text-gray-400">Your cart is empty.</p>
            ) : (
              <>
                {cart.map(item => (
                  <CartItem 
                    key={item.id} 
                    item={item} 
                    increaseQuantity={increaseQuantity}
                    decreaseQuantity={decreaseQuantity}
                  />
                ))}
                <div className="text-right font-bold text-lg mt-4">
                  Total: {formatPrice(total)}
                </div>
              </>
            )}
          </div>
          <CheckoutForm processPayment={processPayment} />
        </div>
      </div>
    </div>
  );
}
