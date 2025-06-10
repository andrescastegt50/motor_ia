from flask import Flask, request, jsonify

app = Flask(__name__)

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

    return jsonify(señal)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
