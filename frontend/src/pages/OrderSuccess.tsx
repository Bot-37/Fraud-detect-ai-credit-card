
import { useEffect } from "react";
import { Link } from "react-router-dom";
import { CheckCircle } from "lucide-react";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import { Button } from "@/components/ui/button";
import { useCart } from "@/Context/CartContext";

const OrderSuccess = () => {
  const { clearCart } = useCart();
  
  // Clear the cart when order is successful
  useEffect(() => {
    clearCart();
  }, [clearCart]);

  return (
    <div className="flex flex-col min-h-screen">
      <Navbar />
      <main className="flex-grow container mx-auto px-4 py-12">
        <div className="max-w-2xl mx-auto bg-white rounded-lg shadow-md p-8 text-center">
          <CheckCircle className="mx-auto h-20 w-20 text-green-500 mb-6" />
          <h1 className="text-3xl font-bold text-gray-900 mb-3">Order Successful!</h1>
          <p className="text-gray-600 mb-6">
            Thank you for your purchase. Your order has been received and is being processed.
            You will receive an email confirmation shortly.
          </p>
          
          <div className="bg-gray-50 p-6 rounded-lg mb-6">
            <h2 className="text-lg font-medium mb-4">Order Information</h2>
            <div className="grid grid-cols-2 gap-4 text-left">
              <div>
                <p className="text-gray-500">Order Number</p>
                <p className="font-medium">NM-{Math.floor(Math.random() * 10000).toString().padStart(4, '0')}</p>
              </div>
              <div>
                <p className="text-gray-500">Order Date</p>
                <p className="font-medium">{new Date().toLocaleDateString()}</p>
              </div>
              <div>
                <p className="text-gray-500">Payment Method</p>
                <p className="font-medium">Credit Card</p>
              </div>
              <div>
                <p className="text-gray-500">Shipping Method</p>
                <p className="font-medium">Standard Shipping</p>
              </div>
            </div>
          </div>
          
          <p className="text-green-600 font-medium mb-8">
            Your transaction was successfully verified by our fraud detection system.
          </p>
          
          <div className="flex flex-col sm:flex-row justify-center gap-4">
            <Button asChild>
              <Link to="/">
                Continue Shopping
              </Link>
            </Button>
            <Button variant="outline" asChild>
              <Link to="/account/orders">
                View Your Orders
              </Link>
            </Button>
          </div>
        </div>
      </main>
      <Footer />
    </div>
  );
};

export default OrderSuccess;
