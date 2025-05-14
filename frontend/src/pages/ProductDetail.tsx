
import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { getProductById } from "@/data/mockData";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import { Button } from "@/components/ui/button";
import { useCart } from "@/Context/CartContext";
import { Product } from "@/components/ProductCard";

const ProductDetail = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [product, setProduct] = useState<Product | null>(null);
  const [quantity, setQuantity] = useState(1);
  const { addItem } = useCart();

  useEffect(() => {
    if (id) {
      const foundProduct = getProductById(id);
      if (foundProduct) {
        setProduct(foundProduct);
      } else {
        navigate("/not-found");
      }
    }
  }, [id, navigate]);

  const handleAddToCart = () => {
    if (product) {
      addItem(product, quantity);
    }
  };

  const increaseQuantity = () => setQuantity(prev => prev + 1);
  const decreaseQuantity = () => setQuantity(prev => (prev > 1 ? prev - 1 : 1));

  if (!product) {
    return (
      <div className="flex flex-col min-h-screen">
        <Navbar />
        <main className="flex-grow container mx-auto px-4 py-8">
          <div className="text-center py-16">
            <div className="animate-pulse">
              <div className="h-8 bg-gray-200 rounded w-1/3 mx-auto mb-4"></div>
              <div className="h-64 bg-gray-200 rounded mb-4"></div>
              <div className="h-4 bg-gray-200 rounded w-1/2 mx-auto mb-2"></div>
              <div className="h-4 bg-gray-200 rounded w-1/4 mx-auto"></div>
            </div>
          </div>
        </main>
        <Footer />
      </div>
    );
  }

  return (
    <div className="flex flex-col min-h-screen">
      <Navbar />
      <main className="flex-grow container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div className="bg-white rounded-lg overflow-hidden shadow-md">
            <img 
              src={product.image} 
              alt={product.name} 
              className="w-full h-[400px] object-cover"
            />
          </div>
          
          <div className="bg-white rounded-lg p-6 shadow-md flex flex-col">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">{product.name}</h1>
            <div className="text-2xl font-bold text-brand-DEFAULT mb-4">
              ${product.price.toFixed(2)}
            </div>
            
            <p className="text-gray-600 mb-6">{product.description}</p>
            
            <div className="flex items-center mb-6">
              <div className="border rounded-md flex items-center mr-4">
                <Button 
                  variant="ghost" 
                  size="sm" 
                  className="px-3 text-lg"
                  onClick={decreaseQuantity}
                  disabled={quantity <= 1}
                >
                  -
                </Button>
                <span className="px-4">{quantity}</span>
                <Button 
                  variant="ghost" 
                  size="sm" 
                  className="px-3 text-lg"
                  onClick={increaseQuantity}
                >
                  +
                </Button>
              </div>
              <Button 
                onClick={handleAddToCart}
                className="bg-brand-accent hover:bg-brand-accent/90 text-white"
              >
                Add to Cart
              </Button>
            </div>
            
            <div className="mt-auto pt-6 border-t">
              <h3 className="font-medium text-gray-900 mb-2">Product Details</h3>
              <ul className="list-disc pl-5 text-gray-600 space-y-1">
                <li>Category: {product.category}</li>
                <li>Product ID: {product.id}</li>
                <li>Shipping: 2-3 business days</li>
                <li>Return Policy: 30 days easy return</li>
              </ul>
            </div>
          </div>
        </div>
      </main>
      <Footer />
    </div>
  );
};

export default ProductDetail;
