import json, config
from flask import Flask, request, jsonify, render_template
from binance.client import Client
from binance.enums import *

app = Flask(__name__)

client = Client(api_key=config.API_KEY, api_secret_key=config.SECRET_KEY, tld='com')

def order(side, quantity, symbol, order_type=ORDER_TYPE_MARKET):
    try:
        print(f"orden de envio {order_type} - {side} {quantity} {symbol}")
        order = client.create_order(symbol=symbol, side=side, type=order_type, quantity=quantity)
    except Exception as e:
        print("una excepcion ocurrio - {}".format(e))
        return False
    
    return order


@app.route("/")
def Welcome():
    return render_template("dashboard.html")


@app.route('/botitas', methods=['POST'])
def botita():
    data = json.loads(request.data)
    if data['passphrase'] != config.WEBHOOK_PASPHRASE:
        return {
            "code": "error",
            "message": "Buen intento, passphrase equivocada"
        }
        
    print(data['ticker'])
    print(data['bar'])
    
    side = data['strategy']['order_action'].upper()
    quantity = data['strategy']['order_contracts'] 
    ticker = data['ticker']
    order_response = order(side, quantity, ticker)
    
    if order_response:
        return {
            "code" : "success",  
            "message" : "orden ejecutada"  
        }
    else:
        print("pedido fallid")
        return {
            "code" : "error",
            "message" : "orden fallida"  
            
        }