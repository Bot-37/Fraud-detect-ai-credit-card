import { Button } from "@/components/ui/button";
import { Link } from "react-router-dom";

interface CartSummaryProps {
  subtotal: number;
  shipping: number;
  tax: number;
  total: number;
  itemCount: number;
}

const CartSummary = ({ subtotal, shipping, tax, total, itemCount }: CartSummaryProps) => {
  return (
    <div className="bg-gray-50 rounded-lg p-6 sticky top-20">
      <h2 className="text-xl font-semibold mb-4">Order Summary</h2>
      <div className="space-y-3">
        <div className="flex justify-between">
          <span className="text-gray-600">Subtotal ({itemCount} items)</span>
          <span>${subtotal.toFixed(2)}</span>
        </div>
        <div className="flex justify-between">
          <span className="text-gray-600">Shipping</span>
          <span>${shipping.toFixed(2)}</span>
        </div>
        <div className="flex justify-between">
          <span className="text-gray-600">Tax</span>
          <span>${tax.toFixed(2)}</span>
        </div>
        <div className="border-t pt-3 mt-3">
          <div className="flex justify-between font-semibold">
            <span>Total</span>
            <span>${total.toFixed(2)}</span>
          </div>
        </div>
      </div>
      <Button 
        className="w-full mt-6 bg-brand-accent hover:bg-brand-accent/90 text-white"
        asChild
        disabled={itemCount === 0}
      >
        <Link to="/checkout">
          Proceed to Checkout
        </Link>
      </Button>
    </div>
  );
};

export default CartSummary;
