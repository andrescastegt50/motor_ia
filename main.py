import asyncio
from ib_insync import IB
import requests
import json
import os

# Configuración general
TELEGRAM_BOT_TOKEN = "7633890350:AAF_OTp1j6zCJIQTmWHQnThzXlcnV5ElkvQ"
TELEGRAM_CHAT_ID = "8192921196"
WEBHOOK_CHATGPT = "https://webhook-chatgpt-1.onrender.com/forward-to-chatgpt"

def enviar_a_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": mensaje
    }
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"❌ Error al enviar a Telegram: {e}")

def enviar_a_chatgpt(data):
    try:
        response = requests.post(WEBHOOK_CHATGPT, json=data)
        print("✅ Datos enviados a ChatGPT:", response.status_code)
    except Exception as e:
        print(f"❌ Error enviando al motor IA: {e}")

def formatear_posicion(p):
    return {
        "symbol": p.contract.symbol,
        "quantity": p.position,
        "avgPrice": p.avgCost,
        "marketPrice": p.marketPrice(),
        "unrealizedPnL": p.unrealizedPNL
    }

def ejecutar_motor_ia():
    ib = IB()
    try:
        ib.connect('127.0.0.1', 7496, clientId=1)
    except Exception as e:
        return f"❌ Error conectando a IBKR: {e}"

    cuenta = ib.managedAccounts()[0]
    portfolio = ib.portfolio()
    posiciones = [formatear_posicion(p) for p in portfolio]

    summary = ib.accountSummary()
    netliq = float(summary.loc['NetLiquidation', 'value'])
    avail_funds = float(summary.loc['AvailableFunds', 'value'])
    day_trades_left = int(summary.loc['DayTradesLeftT+1', 'value'])

    info = {
        "cuenta": cuenta,
        "valor_portafolio": round(netliq, 2),
        "fondos_disponibles": round(avail_funds, 2),
        "day_trades_disponibles": day_trades_left,
        "posiciones": posiciones,
        "monitorear": ["BTC", "ETH", "XRP", "GLD", "SLV", "XLE", "QQQ", "SMCI", "CELH", "PLTR", "NVDA", "TSLA", "NOC", "LMT", "BABA", "JD", "MSFT", "AAPL"]
    }

    # Enviar a ChatGPT (análisis avanzado)
    enviar_a_chatgpt(info)

    # Enviar resumen a Telegram
    mensaje = f"📊 Portafolio actual (${netliq:.2f})\n"
    mensaje += f"💰 Cash disponible: ${avail_funds:.2f}\n🧾 Day trades restantes: {day_trades_left}\n"
    for p in posiciones:
        mensaje += f"• {p['symbol']}: {p['quantity']} @ {p['avgPrice']} → {p['marketPrice']} | PnL: {round(p['unrealizedPnL'], 2)}\n"
    enviar_a_telegram(mensaje)

    ib.disconnect()
    return "✅ Motor IA ejecutado correctamente."
