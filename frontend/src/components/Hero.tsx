
import { Button } from "@/components/ui/button";
import { Link } from "react-router-dom";

const Hero = () => {
  return (
    <div className="relative bg-gradient-to-r from-brand-DEFAULT to-brand-secondary text-white py-16 md:py-24">
  {/* Add a dark overlay */}
  <div className="absolute inset-0 bg-black/50 z-0"></div>
  <div className="container mx-auto px-4 relative z-10">
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
</div>
  );
};

export default Hero;
