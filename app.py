from flask import Flask, jsonify
from main import ejecutar_motor_ia

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "✅ Motor IA activo."

@app.route("/run", methods=["GET"])
def run_motor():
    resultado = ejecutar_motor_ia()
    return jsonify({"status": "ok", "mensaje": resultado})

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render usa la variable de entorno PORT
    app.run(host="0.0.0.0", port=port)