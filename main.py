import json
import requests
from ib_insync import IB, util

def ejecutar_motor_ia():
    ib = IB()
    ib.connect('127.0.0.1', 7496, clientId=1)

    # Obtener portafolio actual
    portfolio = ib.portfolio()

    positions_data = []
    for pos in portfolio:
        symbol = pos.contract.symbol
        shares = pos.position
        avg_price = pos.avgCost
        asset_type = 'stock' if pos.contract.secType == 'STK' else 'etf'

        positions_data.append({
            "symbol": symbol,
            "shares": shares,
            "entry": round(avg_price, 2),
            "type": asset_type
        })

    # Resumen de cuenta
    account_summary = ib.accountSummary()
    cash = float(account_summary.loc['NetLiquidation', 'value'])
    available_funds = float(account_summary.loc['AvailableFunds', 'value'])

    # Watchlists
    crypto_watchlist = ["BTC", "ETH", "XRP"]
    sector_watchlist = ["semiconductors", "AI", "military", "commodities", "NASDAQ"]

    # Construir payload
    data = {
        "portfolio": positions_data,
        "cash_available": round(available_funds, 2),
        "margin_enabled": True,
        "margin_multiplier": 2.0,
        "risk_profile": "high",
        "day_trades_left": 2,
        "open_trades_today": 1,
        "crypto_watchlist": crypto_watchlist,
        "sector_watchlist": sector_watchlist
    }

    try:
        response = requests.post("https://webhook-chatgpt-1.onrender.com/forward-to-chatgpt",
                                 headers={"Content-Type": "application/json"},
                                 data=json.dumps(data))
        print(f"✅ Enviado al motor IA. Código: {response.status_code}")
        print("🧠 Respuesta:", response.text)
        return response.text
    except Exception as e:
        print("❌ Error al enviar datos al motor IA:", e)
        return f"Error: {e}"

    finally:
        ib.disconnect()
