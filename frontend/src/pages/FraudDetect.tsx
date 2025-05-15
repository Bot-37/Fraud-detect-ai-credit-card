import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import FraudDetectionForm from "@/components/FraudDetectionForm";

const SecurityPage = () => {
  return (
    <div className="flex flex-col min-h-screen">
      <Navbar />
      <main className="flex-grow">
        <div className="bg-gradient-to-r from-brand-DEFAULT to-brand-secondary text-gray-900 py-16">
          <div className="container mx-auto px-4">
            <h1 className="text-4xl font-bold mb-4 text-center">Fraud Detection Service</h1>
            <p className="text-xl opacity-90 text-center mb-8">
              Enter transaction details below to check for fraud risk.
            </p>
            <FraudDetectionForm />
          </div>
        </div>
      </main>
      <Footer />
    </div>
  );
};

export default SecurityPage;