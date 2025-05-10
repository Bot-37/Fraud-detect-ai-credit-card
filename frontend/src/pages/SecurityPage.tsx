
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import { Shield, Lock, AlertTriangle, CheckCircle } from "lucide-react";

const SecurityPage = () => {
  return (
    <div className="flex flex-col min-h-screen">
      <Navbar />
      <main className="flex-grow">
        <div className="bg-gradient-to-r from-brand-DEFAULT to-brand-secondary text-white py-16">
          <div className="container mx-auto px-4">
            <div className="max-w-3xl mx-auto text-center">
              <Shield className="mx-auto h-16 w-16 mb-6" />
              <h1 className="text-4xl font-bold mb-4">Fraud Detection & Security</h1>
              <p className="text-xl opacity-90">
                Learn how Naan Mudhalavan Shopping protects your transactions with advanced fraud detection systems.
              </p>
            </div>
          </div>
        </div>
        
        <section className="py-16 bg-white">
          <div className="container mx-auto px-4">
            <div className="max-w-3xl mx-auto">
              <h2 className="text-3xl font-bold mb-6">Our Security Approach</h2>
              <p className="text-gray-600 mb-8">
                At Naan Mudhalavan Shopping, we take your security seriously. Our advanced fraud detection system 
                analyzes each transaction in real-time to identify and prevent fraudulent activities, giving you peace 
                of mind while shopping with us.
              </p>
              
              <div className="grid md:grid-cols-2 gap-8 mb-16">
                <div className="bg-gray-50 p-6 rounded-lg">
                  <div className="flex items-center mb-4">
                    <Lock className="h-8 w-8 text-brand-DEFAULT mr-3" />
                    <h3 className="text-xl font-semibold">Secure Transactions</h3>
                  </div>
                  <p className="text-gray-600">
                    All payment information is encrypted using industry-standard SSL technology. Your credit card 
                    details are never stored on our servers.
                  </p>
                </div>
                
                <div className="bg-gray-50 p-6 rounded-lg">
                  <div className="flex items-center mb-4">
                    <AlertTriangle className="h-8 w-8 text-brand-DEFAULT mr-3" />
                    <h3 className="text-xl font-semibold">Fraud Detection</h3>
                  </div>
                  <p className="text-gray-600">
                    Our advanced AI-powered fraud detection system analyzes multiple data points to identify 
                    suspicious activities and protect your account.
                  </p>
                </div>
              </div>
              
              <h2 className="text-3xl font-bold mb-6">How Our Fraud Detection Works</h2>
              
              <div className="space-y-8 mb-16">
                <div className="flex items-start">
                  <div className="bg-brand-DEFAULT rounded-full p-2 text-white mr-4 mt-1">
                    <CheckCircle className="h-5 w-5" />
                  </div>
                  <div>
                    <h3 className="text-xl font-semibold mb-2">Real-time Transaction Analysis</h3>
                    <p className="text-gray-600">
                      When you make a purchase, our system instantly analyzes various aspects of the transaction, 
                      including purchase amount, location, device information, and historical patterns.
                    </p>
                  </div>
                </div>
                
                <div className="flex items-start">
                  <div className="bg-brand-DEFAULT rounded-full p-2 text-white mr-4 mt-1">
                    <CheckCircle className="h-5 w-5" />
                  </div>
                  <div>
                    <h3 className="text-xl font-semibold mb-2">Machine Learning Models</h3>
                    <p className="text-gray-600">
                      Our fraud detection utilizes advanced machine learning algorithms that continuously improve 
                      and adapt to new threats and patterns of fraudulent behavior.
                    </p>
                  </div>
                </div>
                
                <div className="flex items-start">
                  <div className="bg-brand-DEFAULT rounded-full p-2 text-white mr-4 mt-1">
                    <CheckCircle className="h-5 w-5" />
                  </div>
                  <div>
                    <h3 className="text-xl font-semibold mb-2">Additional Verification</h3>
                    <p className="text-gray-600">
                      For suspicious transactions, additional verification steps may be required to ensure the 
                      legitimacy of the purchase and protect your account.
                    </p>
                  </div>
                </div>
                
                <div className="flex items-start">
                  <div className="bg-brand-DEFAULT rounded-full p-2 text-white mr-4 mt-1">
                    <CheckCircle className="h-5 w-5" />
                  </div>
                  <div>
                    <h3 className="text-xl font-semibold mb-2">Integration with fraud_detector.py</h3>
                    <p className="text-gray-600">
                      Our system integrates with a specialized Python-based fraud detection engine that provides 
                      in-depth analysis and risk scoring for each transaction.
                    </p>
                  </div>
                </div>
              </div>
              
              <div className="bg-gray-50 p-8 rounded-lg border border-gray-200">
                <h3 className="text-xl font-semibold mb-4">Technical Implementation</h3>
                <p className="text-gray-600 mb-4">
                  Our e-commerce platform connects to the fraud detection system through a secure API. When a customer 
                  makes a purchase, the following process occurs:
                </p>
                <ol className="list-decimal pl-5 space-y-2 text-gray-600">
                  <li>Transaction details are securely sent to server.py</li>
                  <li>server.py processes the data and forwards it to fraud_detector.py</li>
                  <li>fraud_detector.py analyzes the transaction using machine learning models</li>
                  <li>A risk score and fraud determination is returned to the e-commerce platform</li>
                  <li>Based on the response, the transaction is either approved, flagged for review, or declined</li>
                </ol>
              </div>
            </div>
          </div>
        </section>
      </main>
      <Footer />
    </div>
  );
};

export default SecurityPage;
