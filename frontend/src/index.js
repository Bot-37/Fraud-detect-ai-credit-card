import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './styles/index.css';        // ← Make sure this line is here
// or import './main.css' if you named it differently

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);
