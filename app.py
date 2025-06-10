from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

def reenviar_a_chatgpt(payload):
    try:
        response = requests.post("https://webhook-chatgpt-1.onrender.com/forward-to-chatgpt", json=payload)
        if response.status_code == 200:
            print("✅ Reenvío exitoso a ChatGPT")
        else:
            print(f"❌ Error en reenvío: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Excepción en reenvío: {e}")

@app.route('/data', methods=['POST'])
def procesar():
    datos = request.get_json()

    # Aquí iría la lógica real del motor IA
    señal = {
        "symbol": "NVDA",
        "action": "BUY",
        "entry": 141.20,
        "tp": 152.00,
        "sl": 137.00,
        "confidence": 85
    }

    # Reenviamos la señal al webhook de ChatGPT
    reenviar_a_chatgpt(señal)

    return jsonify(señal)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
