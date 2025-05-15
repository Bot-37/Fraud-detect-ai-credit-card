//component/Navbar.tsx

import { useState } from "react";
import { Link } from "react-router-dom";
import { ShoppingCart, Menu, X, Search } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

const Navbar = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [cartItemCount, setCartItemCount] = useState(0);

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  return (
    <nav className="bg-white shadow-md sticky top-0 z-50">
      <div className="container mx-auto px-4 py-3">
        <div className="flex items-center justify-between">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-2">
            <span className="text-2xl font-bold text-brand-DEFAULT">Naan Mudhalavan Shopping</span>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-8">
            <div className="relative w-64">
              <Input 
                type="text" 
                placeholder="Search products..." 
                className="pl-10 pr-4"
              />
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
            </div>
            <Link to="/categories" className="text-gray-700 hover:text-brand-DEFAULT">Categories</Link>
            <Link to="/deals" className="text-gray-700 hover:text-brand-DEFAULT">Deals</Link>
            <Link to="/new" className="text-gray-700 hover:text-brand-DEFAULT">New Arrivals</Link>
            <Link to="/cart" className="relative">
              <ShoppingCart className="h-6 w-6 text-gray-700 hover:text-brand-DEFAULT" />
              {cartItemCount > 0 && (
                <span className="absolute -top-2 -right-2 bg-brand-accent text-white text-xs rounded-full h-5 w-5 flex items-center justify-center">
                  {cartItemCount}
                </span>
              )}
            </Link>
          </div>

          {/* Mobile Navigation Toggle */}
          <div className="md:hidden flex items-center">
            <Link to="/cart" className="relative mr-4">
              <ShoppingCart className="h-6 w-6 text-gray-700" />
              {cartItemCount > 0 && (
                <span className="absolute -top-2 -right-2 bg-brand-accent text-white text-xs rounded-full h-5 w-5 flex items-center justify-center">
                  {cartItemCount}
                </span>
              )}
            </Link>
            <Button onClick={toggleMenu} variant="ghost" size="icon">
              {isMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
            </Button>
          </div>
        </div>

        {/* Mobile Menu */}
        {isMenuOpen && (
          <div className="md:hidden py-4 animate-fade-in">
            <div className="flex items-center mb-4">
              <Input type="text" placeholder="Search products..." className="w-full" />
              <Button size="sm" className="ml-2">
                <Search className="h-4 w-4" />
              </Button>
            </div>
            <div className="flex flex-col space-y-3">
              <Link to="/categories" className="text-gray-700 hover:text-brand-DEFAULT py-2 px-3 rounded-md hover:bg-gray-100">
                Categories
              </Link>
              <Link to="/deals" className="text-gray-700 hover:text-brand-DEFAULT py-2 px-3 rounded-md hover:bg-gray-100">
                Deals
              </Link>
              <Link to="/new" className="text-gray-700 hover:text-brand-DEFAULT py-2 px-3 rounded-md hover:bg-gray-100">
                New Arrivals
              </Link>
            </div>
          </div>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
