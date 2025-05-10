
import { Button } from "@/components/ui/button";
import { Link } from "react-router-dom";

const Hero = () => {
  return (
    <div className="relative bg-gradient-to-r from-brand-DEFAULT to-brand-secondary text-white py-16 md:py-24">
      <div className="container mx-auto px-4">
        <div className="max-w-2xl space-y-6">
          <h1 className="text-4xl md:text-5xl font-bold leading-tight">
            Shop Securely with Naan Mudhalavan
          </h1>
          <p className="text-lg md:text-xl opacity-90">
            Experience safe and secure shopping with our advanced fraud detection system.
            Browse our wide selection of products with peace of mind.
          </p>
          <div className="flex flex-wrap gap-4">
            <Button 
              size="lg" 
              asChild
              className="bg-brand-accent hover:bg-brand-accent/90 text-white"
            >
              <Link to="/categories">
                Shop Now
              </Link>
            </Button>
            <Button 
              size="lg" 
              variant="outline"
              asChild
              className="bg-transparent border-white text-white hover:bg-white/10"
            >
              <Link to="/security">
                Learn About Our Security
              </Link>
            </Button>
          </div>
        </div>
      </div>
      <div className="absolute right-0 bottom-0 w-1/3 h-full opacity-10">
        {/* Pattern or background decoration could go here */}
      </div>
    </div>
  );
};

export default Hero;
