
import { createContext, useContext, useState, useEffect, ReactNode } from "react";
import { Product } from "../components/ProductCard";
import { CartItem } from "../components/Cart/CartItem";

interface CartContextType {
  items: CartItem[];
  addItem: (product: Product, quantity?: number) => void;
  removeItem: (id: string) => void;
  updateQuantity: (id: string, quantity: number) => void;
  clearCart: () => void;
  itemCount: number;
  subtotal: number;
  tax: number;
  shipping: number;
  total: number;
}

const CartContext = createContext<CartContextType | undefined>(undefined);

export const useCart = () => {
  const context = useContext(CartContext);
  if (!context) {
    throw new Error("useCart must be used within a CartProvider");
  }
  return context;
};

interface CartProviderProps {
  children: ReactNode;
}

export const CartProvider = ({ children }: CartProviderProps) => {
  const [items, setItems] = useState<CartItem[]>([]);
  const [itemCount, setItemCount] = useState(0);
  const [subtotal, setSubtotal] = useState(0);
  
  const TAX_RATE = 0.18; // 18% GST
  const SHIPPING_FEE = subtotal > 0 ? (subtotal > 1000 ? 0 : 50) : 0; // Free shipping over ₹1000
  
  useEffect(() => {
    // Calculate item count and subtotal whenever items change
    const count = items.reduce((total, item) => total + item.quantity, 0);
    const amount = items.reduce((total, item) => total + (item.product.price * item.quantity), 0);
    
    setItemCount(count);
    setSubtotal(amount);
  }, [items]);
  
  const tax = subtotal * TAX_RATE;
  const shipping = SHIPPING_FEE;
  const total = subtotal + tax + shipping;
  
  const addItem = (product: Product, quantity = 1) => {
    setItems((prevItems) => {
      const existingItemIndex = prevItems.findIndex(item => item.product.id === product.id);
      
      if (existingItemIndex >= 0) {
        // If item exists, update quantity
        const updatedItems = [...prevItems];
        updatedItems[existingItemIndex].quantity += quantity;
        return updatedItems;
      } else {
        // If item doesn't exist, add new item
        return [...prevItems, { product, quantity }];
      }
    });
  };
  
  const removeItem = (id: string) => {
    setItems(prevItems => prevItems.filter(item => item.product.id !== id));
  };
  
  const updateQuantity = (id: string, quantity: number) => {
    setItems(prevItems => 
      prevItems.map(item => 
        item.product.id === id ? { ...item, quantity } : item
      )
    );
  };
  
  const clearCart = () => {
    setItems([]);
  };
  
  return (
    <CartContext.Provider value={{
      items,
      addItem,
      removeItem,
      updateQuantity,
      clearCart,
      itemCount,
      subtotal,
      tax,
      shipping,
      total
    }}>
      {children}
    </CartContext.Provider>
  );
};
