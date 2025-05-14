import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import CartItem from "@/components/Cart/CartItem";
import CartSummary from "@/components/Cart/CartSummary";
import { useCart } from "@/Context/CartContext";
import { Button } from "@/components/ui/button";
import { ShoppingBag } from "lucide-react";
import { Link } from "react-router-dom";

const CartPage = () => {
  const { items, removeItem, updateQuantity, itemCount, subtotal, shipping, tax, total } = useCart();

  return (
    <div className="flex flex-col min-h-screen">
      <Navbar />
      <main className="flex-grow container mx-auto px-4 py-8">
        <h1 className="text-2xl font-bold mb-6">Shopping Cart</h1>
        
        {items.length === 0 ? (
          <div className="text-center py-16 bg-white rounded-lg shadow-md">
            <ShoppingBag className="mx-auto h-16 w-16 text-gray-400 mb-4" />
            <h2 className="text-xl font-medium text-gray-900 mb-2">Your cart is empty</h2>
            <p className="text-gray-600 mb-6">Looks like you haven't added any products to your cart yet.</p>
            <Button asChild>
              <Link to="/">Continue Shopping</Link>
            </Button>
          </div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <div className="lg:col-span-2">
              <div className="bg-white rounded-lg shadow-md p-6">
                <div className="space-y-1">
                  {items.map((item) => (
                    <CartItem
                      key={item.product.id}
                      item={item}
                      onUpdateQuantity={updateQuantity}
                      onRemove={removeItem}
                    />
                  ))}
                </div>
                
                <div className="mt-6 flex justify-between items-center">
                  <Button variant="outline" asChild>
                    <Link to="/">Continue Shopping</Link>
                  </Button>
                </div>
              </div>
            </div>
            
            <div className="lg:col-span-1">
              <CartSummary
                subtotal={subtotal}
                shipping={shipping}
                tax={tax}
                total={total}
                itemCount={itemCount}
              />
            </div>
          </div>
        )}
      </main>
      <Footer />
    </div>
  );
};

export default CartPage;
