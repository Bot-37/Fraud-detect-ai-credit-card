
import { useState } from "react";
import Navbar from "@/components/Navbar";
import Hero from "@/components/Hero";
import FeaturedProducts from "@/components/FeaturedProducts";
import CategoryList from "@/components/CategoryList";
import Footer from "@/components/Footer";
import { mockProducts, categories } from "@/data/mockData";
import { useCart } from "@/context/CartContext";
import { Product } from "@/components/ProductCard";

const Index = () => {
  const { addItem } = useCart();
  const featuredProducts = mockProducts.slice(0, 4); // Show first 4 products as featured
  
  const handleAddToCart = (product: Product) => {
    addItem(product, 1);
  };

  return (
    <div className="flex flex-col min-h-screen">
      <Navbar />
      <main className="flex-grow">
        <Hero />
        <FeaturedProducts 
          products={featuredProducts} 
          onAddToCart={handleAddToCart} 
        />
        <CategoryList categories={categories} />
      </main>
      <Footer />
    </div>
  );
};

export default Index;
