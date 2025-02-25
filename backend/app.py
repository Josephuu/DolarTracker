from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:30423"],  # Ajusta según la URL del frontend en Minikube
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mapeo de nombres de la API a nombres personalizados
DOLLAR_MAPPING = {
    "oficial": "oficial",
    "blue": "blue",
    "bolsa": "mep",
    "contado con liquidación": "ccl",
    "mayorista": "mayorista",
    "cripto": "cripto",
    "tarjeta": "turista"
}

def get_dollar_rates():
    url = "https://dolarapi.com/v1/dolares"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        rates = {}
        for dollar in data:
            # Usar el nombre original de la API
            api_name = dollar["nombre"].lower().replace("dólar ", "")
            # Mapear al nombre que queremos en el frontend
            mapped_name = DOLLAR_MAPPING.get(api_name, api_name)
            rates[mapped_name] = {
                "compra": dollar["compra"],
                "venta": dollar["venta"]
            }
        return rates
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con la API: {e}")
        return {
            "oficial": {"compra": 950, "venta": 1000},
            "blue": {"compra": 1200, "venta": 1250},
            "mep": {"compra": 1150, "venta": 1180},
            "ccl": {"compra": 1170, "venta": 1200},
            "turista": {"compra": None, "venta": 1600}
        }

@app.get("/api/dollars")
async def dollars():
    rates = get_dollar_rates()
    return rates

# Ejecutar con: uvicorn app:app --reload