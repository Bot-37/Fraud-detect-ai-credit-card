
import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { getProductsByCategory, categories } from "@/data/mockData";
import { Product } from "@/components/ProductCard";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import ProductCard from "@/components/ProductCard";
import { useCart } from "@/Context/CartContext";

const CategoryPage = () => {
  const { id } = useParams<{ id: string }>();
  const [products, setProducts] = useState<Product[]>([]);
  const [categoryName, setCategoryName] = useState("");
  const { addItem } = useCart();

  useEffect(() => {
    if (id) {
      const categoryProducts = getProductsByCategory(id);
      setProducts(categoryProducts);
      
      const category = categories.find(cat => cat.id === id);
      setCategoryName(category?.name || "");
    }
  }, [id]);

  const handleAddToCart = (product: Product) => {
    addItem(product, 1);
  };

  return (
    <div className="flex flex-col min-h-screen">
      <Navbar />
      <main className="flex-grow">
        <div className="bg-gradient-to-r from-brand-DEFAULT to-brand-secondary text-white py-12">
          <div className="container mx-auto px-4">
            <h1 className="text-3xl font-bold">{categoryName}</h1>
          </div>
        </div>
        
        <section className="py-12">
          <div className="container mx-auto px-4">
            {products.length > 0 ? (
              <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
                {products.map((product) => (
                  <ProductCard
                    key={product.id}
                    product={product}
                    onAddToCart={handleAddToCart}
                  />
                ))}
              </div>
            ) : (
              <div className="text-center py-16">
                <p className="text-xl text-gray-600">
                  No products found in this category.
                </p>
              </div>
            )}
          </div>
        </section>
      </main>
      <Footer />
    </div>
  );
};

export default CategoryPage;
