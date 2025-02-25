import React, { useEffect, useState } from 'react';
import './App.css';

function App() {
  const [rates, setRates] = useState({});

  useEffect(() => {
    fetch('/api/dollars') // Asegúrate de que sea esta ruta
      .then(response => response.json())
      .then(data => setRates(data))
      .catch(error => console.error('Error fetching data:', error));
  }, []);

  return (
    <div className="App">
      <h1>Tipos de Dólar en Argentina</h1>
      <div className="dollar-list">
        {Object.keys(rates).map((type) => (
          <div key={type} className="dollar-card">
            <h2>Dólar {type.charAt(0).toUpperCase() + type.slice(1)}</h2>
            <p>Compra: <span>${rates[type].compra || '-'}</span></p>
            <p>Venta: <span>${rates[type].venta || '-'}</span></p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;