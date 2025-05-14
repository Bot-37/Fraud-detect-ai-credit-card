import { useState } from "react";
import { Trash2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Product } from "@/components/ProductCard";
import { useToast } from "@/hooks/use-toast";

interface CartItemProps {
  item: CartItem;
  onUpdateQuantity: (id: string, quantity: number) => void;
  onRemove: (id: string) => void;
}

export interface CartItem {
  product: Product;
  quantity: number;
}

const CartItem = ({ item, onUpdateQuantity, onRemove }: CartItemProps) => {
  const { product, quantity } = item;
  const { toast } = useToast();
  
  const handleRemove = () => {
    onRemove(product.id);
    toast({
      title: "Item removed",
      description: `${product.name} has been removed from your cart.`,
      duration: 3000,
    });
  };

  const handleQuantityChange = (newQuantity: number) => {
    if (newQuantity > 0) {
      onUpdateQuantity(product.id, newQuantity);
    }
  };

  return (
    <div className="flex flex-col sm:flex-row border-b py-4 gap-4">
      <div className="sm:w-28 sm:h-28 w-full h-40">
        <img 
          src={product.image} 
          alt={product.name}
          className="w-full h-full object-cover rounded-md"
        />
      </div>
      <div className="flex-grow flex flex-col">
        <div className="flex justify-between items-start">
          <h3 className="font-medium text-gray-900">{product.name}</h3>
          <Button 
            variant="ghost" 
            size="sm"
            onClick={handleRemove}
            className="text-gray-500 hover:text-destructive p-0 h-auto"
          >
            <Trash2 className="h-4 w-4" />
          </Button>
        </div>
        <p className="text-sm text-gray-600">${product.price.toFixed(2)}</p>
        <div className="flex items-center mt-auto pt-2">
          <div className="flex items-center border rounded-md">
            <Button 
              variant="ghost" 
              size="sm" 
              className="px-2 text-lg"
              onClick={() => handleQuantityChange(quantity - 1)}
              disabled={quantity <= 1}
            >
              -
            </Button>
            <span className="px-3">{quantity}</span>
            <Button 
              variant="ghost" 
              size="sm" 
              className="px-2 text-lg"
              onClick={() => handleQuantityChange(quantity + 1)}
            >
              +
            </Button>
          </div>
          <span className="ml-auto font-medium">
            ${(product.price * quantity).toFixed(2)}
          </span>
        </div>
      </div>
    </div>
  );
};

export default CartItem;
