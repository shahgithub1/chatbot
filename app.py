
from flask import Flask, render_template, jsonify, request
import json

app = Flask(__name__)

# Load stock data from the JSON file
with open('(TC3)Chatbot - stock data.json') as f:
    stock_data = json.load(f)

# Helper function to get stocks by exchange code
def get_stocks_by_exchange(exchange_code):
    for exchange in stock_data:
        if exchange['code'] == exchange_code:
            return exchange['topStocks']
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_stocks', methods=['POST'])
def get_stocks():
    exchange = request.json.get('exchange')
    stocks = get_stocks_by_exchange(exchange)
    if stocks:
        return jsonify(stocks)
    else:
        return jsonify({'error': 'Exchange not found'}), 404

@app.route('/get_stock_price', methods=['POST'])
def get_stock_price():
    exchange = request.json.get('exchange')
    stock_name = request.json.get('stock_name')

    stocks = get_stocks_by_exchange(exchange)
    if stocks:
        for stock in stocks:
            if stock['stockName'] == stock_name:
                return jsonify({'price': stock['price']})
        return jsonify({'error': 'Stock not found'}), 404
    else:
        return jsonify({'error': 'Exchange not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
